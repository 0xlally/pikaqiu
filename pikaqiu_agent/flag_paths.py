from __future__ import annotations


FLAG_HTTP_PATH_CANDIDATES: tuple[str, ...] = (
    "/flag",
    "/FLAG",
    "/flag/",
    "/FLAG/",
    "/flag.txt",
    "/FLAG.txt",
    "/flag.php",
    "/FLAG.php",
    "/flag.html",
    "/FLAG.html",
    "/ctf",
    "/CTF",
    "/ctf.txt",
    "/CTF.txt",
)

FLAG_FILE_PATH_CANDIDATES: tuple[str, ...] = (
    "/flag",
    "/FLAG",
    "/flag.txt",
    "/FLAG.txt",
    "/flag.php",
    "/FLAG.php",
    "/app/flag",
    "/app/FLAG",
    "/app/flag.txt",
    "/app/FLAG.txt",
    "/app/flag.php",
    "/app/FLAG.php",
    "/var/www/flag",
    "/var/www/FLAG",
    "/var/www/flag.txt",
    "/var/www/FLAG.txt",
    "/var/www/html/flag",
    "/var/www/html/FLAG",
    "/var/www/html/flag.txt",
    "/var/www/html/FLAG.txt",
    "/var/www/html/flag.php",
    "/var/www/html/FLAG.php",
    "/tmp/flag",
    "/tmp/FLAG",
    "/home/ctf/flag",
    "/home/ctf/flag.txt",
)

FLAG_HTTP_PATH_HINT = " ".join(FLAG_HTTP_PATH_CANDIDATES)
FLAG_FILE_CAT_COMMAND = "cat " + " ".join(FLAG_FILE_PATH_CANDIDATES) + " 2>/dev/null"
FLAG_FILE_FIND_COMMAND = "find / -maxdepth 4 -iname '*flag*' -type f 2>/dev/null"
FLAG_FILE_GREP_COMMAND = "grep -Rai 'flag{' /app/ /var/www/ /opt/ /tmp/ 2>/dev/null"
