# Playback Extras 0.6.0 — experimental release candidate

This is a proposed prerelease for Sony α6700 (ILCE-6700), Body 2.00. It adds the general **FTP Transfer** playback shortcut alongside the existing **FTP Trans. (This Img.)** action. Both actions remain experimental, and this body has not been tested with this build.

## Scope

- General **FTP Transfer** opens the native selection/progress action for C1/C2. The experimental writer uses two App-only inspection windows, preserves the current-image row, and changes one logical App byte at file offset `0x03788dc3`. It does not access WBI.
- **FTP Trans. (This Img.)** remains a separate current-image action.
- The bundle also retains a separate FTP success-label change that writes WBI, plus an offline-only playback-filter candidate preparation feature. Neither is required for the general shortcut.

## Evidence and limitations

- Python 3.10.20 / PyInstaller 6.22.3 build.
- The implementation source commit is `c5b91087a60bcd613df9c8b4b159a88f6ab9a9e7`; `BUILD.json` hashes every source file included in the bundle.
- The build manifest records a dirty working tree because other local work remained outside the packaged source set.
- Ten frozen offline checks and the full archive member/hash audit passed.
- 157 focused offline unit tests passed.
- `camera_tested` is `false`. Menu assignment, persistence after restart, actual transfer behavior, and receipt hashes are unverified.
- The logical byte count does not prove the physical flash-write extent. Saved preimages are partial; recovery after a failed startup is unproven.
- Before a camera operation, configure `SONY_A6700_PLAYBACK_EXTRAS_SECONDARY_BACKUP` to an absolute directory on a separate local fixed drive. The writer stops if this is missing or does not identify a separate fixed drive.

## Prepared assets

The release assets are prepared locally for upload after this public release PR is reviewed and approved:

- `SonyA6700PlaybackExtrasExperimental_0.6.0.zip`
- `SonyA6700PlaybackExtrasExperimental.exe`

The prepared ZIP is 21,251,675 bytes and the EXE is 3,783,364 bytes.

See `SHA256SUMS.txt` and `BUILD.json` for the exact asset hashes and build provenance. This PR contains release documentation and provenance; the binary is not committed into the Git tree.
