# FT-101: Playback FTP Custom Key Action Discovery

Date: 2026-10-31  
Evidence: **static-inference**, **offline-tested**  
Camera commands: **none**

## Summary

This session traced the exact mechanism preventing the Playback ("browser gallery") custom button from uploading images to FTP on the Sony α6700 (firmware 2.00).

1. In the official mainland firmware application binary (`/lib/appFw.so`, 89,027,992 bytes, SHA-256 `e65fd595052be5d0e98ce8000dfcb94f90a2f8309de70ef140375052009b0ef3`), the action for Playback image transmission is **ActionID `0x0817` (`FTP_TRANSFER`)**, bound at file offset `0x03666b70` to string resource `0x021c668e` ("FTP Transfer" / "FTP传输") and description `0x021c627a` ("将影像优先传输至FTP服务器。播放影像并按自定义键，即可传输影像...").
2. The model capability table in `appFw.so` contains an 8-byte entry for Action `0x0817` at file offset **`0x03f17ce0` (Sector 129214)**. Byte 4 (`0x03f17ce4`) is factory-configured to `0x00` (disabled on ILCE-6700).
3. Upstream projects (Powerful6700-Windows) patched Network Menu settings `0x05a5`–`0x05b0` at `0x03f17524`–`0x03f17564` (Sector 129210), but completely omitted the Action capability entries in Sector 129214.
4. Because `0x03f17ce4` is `0x00`, the Playback Custom Key selection UI (`\ue804Custom Key Setting`, Menu `0x02aa`) treats `FTP_TRANSFER` as unsupported, suppressing it from assignable button options (C1, C2, Delete, etc.).
5. Toggling `0x03f17ce4` from `0x00` to `0x01` enables Action `0x0817` as a supported capability on the camera, solving the missing gallery button trigger.
