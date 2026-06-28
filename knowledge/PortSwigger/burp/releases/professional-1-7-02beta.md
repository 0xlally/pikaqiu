# Professional 1.7.02beta

Source: https://portswigger.net/burp/releases/professional-1-7-02beta
Fetched: 2026-06-28T09:16:28.117387+00:00

This release improves the resilience of disk-based projects in situations where the operating system terminates abnormally.

Burp uses memory-mapped files for disk-based projects. The operating system has responsibility for synchronizing data held in memory with files on disk, and ensures eventual consistency even if an individual process crashes. However, if the operating system itself crashes, then some in-memory data may not be written to disk, leading to a partially corrupted project file. Burp now tries to reduce the impact of this event, by forcing the operating system to write to disk more frequently, and by reopening project files in a more fault-tolerant manner. We are continuing to investigate ways of avoiding data loss in the event of the operating system terminating abnormally, and expect to make further enhancements in future releases. For this reason only, we are continuing to describe the disk-based projects feature as being in beta.
