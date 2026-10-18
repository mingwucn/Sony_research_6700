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

During the original source review, that asset was **not requested**, even with
HEAD. The later consented GET and stopped redirect are recorded below. Use the
official landing-page workflow for approved acquisition; the recorded URL is
provenance, not a substitute for agreement review. `fm=cn` does not prove a distinct regional
binary, equality with another market's bytes, or the installed body's build.
No published firmware digest was observed in the inspected page/selected metadata.
Current acquisition status is recorded below. A later
[scoped UFU directory audit](UFU_CONTAINER_AUDIT.md) records framing metadata;
component formats and source/binary correspondence remain unestablished.

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
| Obtain a normal download and record its size/hash | Limited terms acceptance, initial stopped GET and separately consented completed destination GET are recorded below. Hashing alone is not treated as synonymous with disassembly. |
| Local structural directory, without content extraction | Narrow statutory assessment and actual bounded result are recorded in the [act/parser audit](UFU_CONTAINER_AUDIT.md). |
| Unpack/decompress the proprietary container, extract resources or statically disassemble programs | A suitable rights basis is unestablished: an express applicable licence, scope-specific permission from an authorized rights holder, or a documented applicable statutory basis. Owner authorization alone does not resolve third-party rights. |
| Inspect separately offered OSS source | Apply each component's accompanying licence and notice. The previous two-source approval remains limited to those two archives. |

This review does not decide enforceability or whether a statutory exception
applies. That depends on the activity and relevant jurisdiction; neither a
blanket prohibition on all private inspection nor blanket clearance for the
full proposed research is established. A protection-bypass step, if ever proposed, requires
its own rights/scope review and is absent from this work.

The exact-model [Help Guide licence page](https://helpguide.sony.net/ilc/2320/v1/zh-cn/contents/1005_license.html)
separately identifies GPLv2/other licensed components and source availability.
Those component rights do not automatically extend to proprietary applications,
language resources or the complete update container. It also describes
product-local licence files; **no camera connection was made to retrieve them**.

## China inspection scope — 2026-10-18

The owner reports **China** as the inspection country and confirms **personal,
noncommercial use**. These facts do not accept the download agreement or grant
analysis rights. The earlier **No / unknown** rights answer remains recorded.

The [Ministry of Justice consolidated Software Protection Regulations](https://xzfg.moj.gov.cn/front/law/detail?LawID=581)
show the 2013 second revision; the [CAC publication](https://www.cac.gov.cn/2013-02/08/c_12648744.htm)
corroborates that text. Relevant provisions, **source-report**:

- Article 6 excludes underlying ideas, processes, methods and mathematical
  concepts from software copyright protection.
- Article 16 gives lawful-copy owners specified loading, protective-backup and
  necessary-modification rights, with restrictions on providing modified copies.
- Article 17 permits specified software use for studying its underlying design
  ideas/principles without copyright-holder permission or payment.
- Article 24 separately addresses deliberate circumvention of protective measures.

**Static-inference:** Article 17 is a concrete candidate basis, not a settled
authorization for this research. The text does not expressly name container
unpacking/static disassembly or resolve Sony contract enforceability. Match the
proposed acts, lawful acquisition, applicable terms and any protection issue to
the claimed basis before that analysis. Personal/noncommercial use is a Sony
download condition; it is not an express condition stated in Article 17.
Neither blanket reverse-engineering permission nor invalidity of Sony's terms
is established. Rights-holder permission remains one possible route. The later
Copyright Law finding below strengthens this statutory assessment; Article 17's
wording alone is not the endpoint of the analysis.

## Express reverse-engineering research provision — 2026-10-18

The [National Copyright Administration's consolidated Copyright Law](https://www.ncac.gov.cn/xxfb/flfg/flfg_532/202103/t20210309_50530.html)
expressly includes **computer-software reverse-engineering research** in
**Article 50(5)**, an exception allowing avoidance of technical measures.
Article 49 preserves statutory exceptions. Article 50's opening conditions
prohibit providing bypass technologies/devices/components to others and
infringing other lawful rights. These are **source-report** findings, not an
implied research grant in Sony's agreement.

The [official corroborating text](https://www.nsfc.gov.cn/p1/2871/2872/69475.html)
also records personal-study/research limitations in Article 24, rights-management
information in Article 51, permission or statutory grounds as alternative
evidence in Article 59, and separate contract liability in Article 61.
The [2020 amending decision](https://www.ncac.gov.cn/xxfb/ywxx/202011/t20201112_47358.html)
sets **2021-06-01** as its effective date; consolidated Article 67 retains the
original law's 1991 date.

**Static-inference:** China provides a specific statutory research route;
Sony's separate written permission is not the only possible basis. Assess
Regulation Article 17 together with Copyright Law Articles 24/49/50 against
each proposed local act. This does not settle reproduction/resource extraction,
Sony contract enforceability, distribution or device modification. Article 50(5)
does not state an interoperability-only purpose requirement. No protection-
bypass procedure is proposed, performed or approved by this finding.

A bounded official-case search found no directly applicable firmware-analysis
holding. The closest [Shanghai court-hosted commentary](https://www.shzcfy.gov.cn/detail.jhtml?id=171144)
mentions Article 17 study while discussing commercial pirated game servers;
it does not decide private firmware disassembly or this agreement. Search
coverage was limited; absence of a located case is not absence of a legal basis.

## Ordinary acquisition and bounded identification

The previous sequencing placed inspection-rights resolution before acquisition.
This is refined: an ordinary download plus size/SHA-256 inventory can be decided
separately from unpacking/disassembly. A hash supplies a byte fingerprint and
transfer/storage consistency; without an independent reference it does not
establish authenticity, analysis permission, exact-body compatibility or recovery.

The concrete proposed acquisition is the official mainland **BODYDATA.DAT**
reference above, declared **1,024,017,848 bytes**, after deliberate acceptance of
the [mainland download agreement](https://service.sony.com.cn/download/firm/00003046.html).
A prepared local helper would make one GET, save only into a new ignored private
folder, enforce the declared size and compare transfer/stored SHA-256 hashes.
It requires a matching explicit consent record, journals before requesting,
records and stops on redirects, retains partial/failure evidence and never
retries automatically. No unpacking, disassembly, execution, camera connection,
driver change, installation or upload is included. The old zero-byte failed
attempt remains evidence and will not be rerun.

The owner subsequently **approved this limited download under the agreement**.
The one GET returned HTTP 302 to:

```text
https://di.update.sony.net/NEX/tF4c94033c/BODYDATA.DAT
```

The helper stopped as scoped: exit 1, zero firmware bytes, no payload file,
`needs_review`, no retry. The empty partial SHA-256 in the private failure
journal is not a firmware identity. The original source/terms review above
describes the earlier pre-request snapshot.

The owner then separately **approved the reviewed destination request**. A fresh
private acquisition made one GET of that exact destination: **HTTP 200, exit 0,
1,024,017,848 bytes**, with no further redirect or retry. Transfer and stored-file
SHA-256 values agree:

```text
d3c7db5b9b40c89b11ecf03addf0f6ff1d9b917acf9f55e46360462e86db847c
```

The original bytes remain private. A reversible Windows read-only attribute was
set with size/mtime unchanged; this is not tamper-proof storage, an independent
backup or recovery proof. The earlier failure and both consent records remain.

The existing authored identification probe then hashed the whole file and
classified at most 4,096 prefix bytes from the same read: **exit 0**,
`sony_ufu_signature_candidate`, `container_not_validated`, `UNVERIFIED`.
Its hash agrees with acquisition. It did not walk container chunks, unpack,
decrypt, disassemble, load or execute firmware. The raw prefix and input path
are omitted from its private JSON report. A signature candidate does not verify
format validity, encryption, signing, component layout, ABI or installed build.
Acquisition and this ordinary identification do not resolve later proprietary
analysis rights or accompanying terms. See [commands/results](sessions/20261018-RA-003-package-law.md).

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

The [act/parser continuation](UFU_CONTAINER_AUDIT.md) documents the narrow
statutory assessment for ordinary local metadata reading, audits the locator
and records an authored bounded directory result. Five chunk spans cover the
input under the reviewed framing; component contents were not interpreted or
output. That assessment does not settle every later extraction/disassembly act.

The later [FDAT/extractor audit](FDAT_EXTRACTOR_AUDIT.md) records a 4,096-byte
in-memory opaque prefix result and source-only candidate pin, with no actual
decoding. The preceding no-payload-interpretation statement describes only the
earlier directory run.

The [decoding plan](FDAT_DECODING_PLAN.md) now records a narrow statutory
rationale for private in-memory format study and a synthetic header validator.
The lack of separate Sony permission alone is not the next blocker; operational
crypto provenance/variant selection and the accepted-contract interaction remain.

**RA-003: audit and pin the minimal crypto dependency and public-constant provenance for a bounded private header-decoding trial.** Full proposed analysis scope,
source/build correspondence and exact-body applicability remain unresolved.
Written rights-holder permission remains one possible route alongside the
documented statutory provisions; it is not the only possible basis.

English resource presence and restriction policy remain unknown; the owner report
of English absence is retained. The prior BusyBox FTP source findings remain
static leads, not native FTP support. FL2/FL3/custom looks remain deferred;
the optional HOST-ASSISTED bridge is separate. Recovery is unestablished and no
device-write gate has passed. Camera commands: **none**.


## Later crypto-provenance continuation (2026-10-18)

The [crypto/source audit](FDAT_CRYPTO_PROVENANCE.md) and
[session result](sessions/20261018-RA-003-crypto-provenance.md) supersede
the preceding next-step statement. The private AES wheel and public constants
source are pinned; eight authored primitive tests passed. No actual firmware
read/decoding or camera action occurred. Constants origin and accepted-contract
interaction remain unresolved, alongside exact-body correspondence/recovery.
One predeclared experimental hypothesis is not a target support profile.
Next single package: **RA-003: implement, synthetically qualify and run one bounded private FDAT header trial for the predeclared CXD90057_k8 hypothesis**. No feature/write gate passed.
