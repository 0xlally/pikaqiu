#!/bin/bash
# TPT Agent systemd 服务安装脚本
# 用法: sudo bash install-service.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
SERVICE_FILE="$SCRIPT_DIR/tpt-agent.service"
TARGET="/etc/systemd/system/tpt-agent.service"
TPT_BIN="/usr/local/bin/tpt"

if [ "$EUID" -ne 0 ]; then
    echo "请使用 sudo 运行: sudo bash $0"
    exit 1
fi

if [ ! -f "$SERVICE_FILE" ]; then
    echo "找不到 $SERVICE_FILE"
    exit 1
fi

# 如果服务正在运行，先停止
if systemctl is-active --quiet tpt-agent 2>/dev/null; then
    echo "停止现有服务..."
    systemctl stop tpt-agent
fi

# 动态更新路径写入 systemd
echo "生成服务配置 (项目路径: $PROJECT_DIR)..."
sed -e "s|WorkingDirectory=.*|WorkingDirectory=$PROJECT_DIR|" \
    -e "s|ExecStart=.*|ExecStart=$PROJECT_DIR/venv/bin/python -m tpt_agent|" \
    "$SERVICE_FILE" > "$TARGET"

systemctl daemon-reload
systemctl enable tpt-agent

# 安装 tpt 全局 CLI
echo "安装 tpt 命令到 $TPT_BIN..."
cat > "$TPT_BIN" << 'TPTEOF'
#!/bin/bash
# TPT Agent 管理工具
SERVICE="tpt-agent"

usage() {
    echo "TPT Agent 管理工具"
    echo ""
    echo "用法: tpt <command>"
    echo ""
    echo "命令:"
    echo "  start       启动服务"
    echo "  stop        停止服务"
    echo "  restart     重启服务"
    echo "  status      查看状态"
    echo "  logs        实时日志 (Ctrl+C 退出)"
    echo "  logs -n N   最近N行日志"
    echo "  update      同步代码后重启"
    echo ""
}

case "${1:-}" in
    start)
        sudo systemctl start "$SERVICE"
        sudo systemctl status "$SERVICE" --no-pager -l
        ;;
    stop)
        sudo systemctl stop "$SERVICE"
        echo "已停止"
        ;;
    restart)
        sudo systemctl restart "$SERVICE"
        sudo systemctl status "$SERVICE" --no-pager -l
        ;;
    status)
        sudo systemctl status "$SERVICE" --no-pager -l
        ;;
    logs)
        shift
        if [ "${1:-}" = "-n" ] && [ -n "${2:-}" ]; then
            sudo journalctl -u "$SERVICE" --no-pager -n "$2"
        else
            sudo journalctl -u "$SERVICE" -f
        fi
        ;;
    update)
        echo "重启服务..."
        sudo systemctl restart "$SERVICE"
        sleep 2
        sudo systemctl status "$SERVICE" --no-pager -l
        ;;
    *)
        usage
        ;;
esac
TPTEOF
chmod +x "$TPT_BIN"

echo ""
echo "安装完成!"
echo ""
echo "使用方式:"
echo "  tpt start       # 启动"
echo "  tpt stop        # 停止"
echo "  tpt restart     # 重启"
echo "  tpt status      # 状态"
echo "  tpt logs        # 实时日志"
echo "  tpt logs -n 50  # 最近50行"
echo "  tpt update      # 代码更新后重启"
echo ""
echo "现在启动: tpt start"