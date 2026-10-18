# RA-003: mainland 2.00 source and inspection rights

Reviewed 2026-10-18. Public findings are **source-report**; the workflow and
rights-basis interpretation below are **static-inference**, not a legal ruling.
English and native camera-to-server Wi-Fi FTP remain primary.

## Official source

[Sony China ILCE-6700 support](https://service.sony.com.cn/products/di/ILCE-6700.html)
offers [Ver.2.00](https://service.sony.com.cn/download/firm/00003046.html).

| Declared field | Observed value |
|---|---|
| Version / release | 2.00 / 2025-06-10 |
| Applicable models | ILCE-6700, ILCE-6700K/L/M |
| File / size | BODYDATA.DAT / 1,024,017,848 bytes |

The page embeds a public
[download-page script](https://service.sony.com.cn/etc/designs/casch/js/clientlib-downloadRoom.js).
Reading it as text identified this
[metadata endpoint](https://service.sony.com.cn/casch/outDownload?method=findOne&path=/etc/commerce/products/casch/pim/download/firmware/00003046).
Its `returnData.Data.downloadPath` array contains:

```text
https://support.d-imaging.sony.co.jp/download/NEX/tF4c94033c/BODYDATA.DAT?fm=cn
```

That asset was **not requested**, even with HEAD. Use the official landing-page
workflow for any later approved acquisition; the recorded URL is provenance,
not a substitute for agreement review. `fm=cn` does not prove a distinct regional
binary, equality with another market's bytes, or the installed body's build.
No published firmware digest was observed in the inspected page/selected metadata.
No payload, payload hash, container inventory or source/binary correspondence exists.

## What permission is needed

The mainland page's **在线下载协议** requires agreement before downloading.
Section 1 limits use to personal/noncommercial purposes; section 3 restricts
modification, decomposition, decompilation, disassembly and reverse engineering.
Section 4 says accompanying EULAs may also apply. No express offline-research
grant or written-consent/OSS exception appears in that download text.
[Source: mainland agreement on the download page](https://service.sony.com.cn/download/firm/00003046.html).

The practical distinction is:

| Activity | Current basis / unresolved point |
|---|---|
| Read public documentation and published metadata | Authorized host-side research; completed |
| Obtain a normal download and record its size/hash | Review and accept applicable download terms deliberately; no acceptance or firmware request occurred here. Hashing alone is not treated as synonymous with disassembly. |
| Unpack/decompress the proprietary container, extract resources or statically disassemble programs | A suitable rights basis is unestablished: an express applicable licence, scope-specific permission from an authorized rights holder, or a documented applicable statutory basis. Owner authorization alone does not resolve third-party rights. |
| Inspect separately offered OSS source | Apply each component's accompanying licence and notice. The previous two-source approval remains limited to those two archives. |

This review does not decide enforceability or whether a statutory exception
applies. That depends on the activity and relevant jurisdiction; neither a
blanket prohibition on all private inspection nor an exception covering this
research is established. A protection-bypass step, if ever proposed, requires
its own rights/scope review and is absent from this work.

The exact-model [Help Guide licence page](https://helpguide.sony.net/ilc/2320/v1/zh-cn/contents/1005_license.html)
separately identifies GPLv2/other licensed components and source availability.
Those component rights do not automatically extend to proprietary applications,
language resources or the complete update container. It also describes
product-local licence files; **no camera connection was made to retrieve them**.

## Prepared inquiry, not sent

[Sony China's contact page](https://service.sony.com.cn/content/casch/contact-us.html)
lists `ccc@sony.com.cn` and 400 810 9000. These are routing channels, not evidence
that a support representative can grant the required rights. Ask for an
authorized firmware/IP contact and a written response with scope and conditions.
Do not attach firmware, dumps, serials or credentials.

Draft for the owner's review:

> 请转交有权处理固件许可/知识产权咨询的团队。本人拥有中国大陆版 ILCE-6700，版本显示为 2.00，拟从索尼中国官方页面取得对应固件，仅在本地进行个人非商业研究，目标是评估原生英文菜单和相机直接通过 Wi-Fi 上传至 FTP 服务器的可行性。请确认是否有适用许可，或可否书面授权为此进行本地复制、容器解包/解压、语言资源提取及程序静态反汇编分析，并说明附带 EULA、第三方组件和任何限制的适用范围。本次申请不涉及连接或修改相机、执行固件、绕过保护、分发固件/提取内容或公开补丁。请提供授权主体、覆盖版本和允许行为的书面说明；如无法授权，请告知可适用的官方研究资料或许可渠道。

No inquiry was sent; sending it requires a separate owner instruction. A generic
support acknowledgement or download approval
would not itself document permission for unpacking/disassembly. Any later
modification, redistribution or device operation remains separately scoped.

## Next single work package

**RA-003: resolve and record the rights basis for mainland 2.00 offline
unpacking/static analysis**, using a scope-specific rights-holder response or
another documented applicable basis. Then plan acquisition under the applicable
terms, preserve immutable bytes/size/hash, and establish source/build
correspondence before choosing an extractor. No additional download is requested
by this report.

English resource presence and restriction policy remain unknown; the owner report
of English absence is retained. The prior BusyBox FTP source findings remain
static leads, not native FTP support. FL2/FL3/custom looks remain deferred;
the optional HOST-ASSISTED bridge is separate. Recovery is unestablished and no
device-write gate has passed. Camera commands: **none**.
