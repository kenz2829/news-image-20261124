# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/kenz2829/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/kenz2829/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A pure-Python program that draws one 1024×1024 picture summing up the world's news on **Tuesday 24 November 2026**: 35 real stories from all 7 regions, 6 key metrics, a world map with numbered pins, and a digest. Built for the make.fun open bounty `news-image-20261124` ($100 USDC prize pool).

## Run it

```sh
python3 -P -s main.py
```

Writes `output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png` when set). Pure standard library only — no Pillow, no network, deterministic output.

---

## The 35 stories — Tuesday 24 November 2026

Every story happened or was first reported on Tuesday 24 November 2026. Contested claims carry explicit attribution in the image and below.

| # | Story | Source |
|---|-------|--------|
| 1 | Iran says four tankers hit mines — IRGC says four tankers hit naval mines in the Strait of Hormuz and caught fire. | AP |
| 2 | Ukraine hits ships in two seas — Kyiv confirms drone strike on Sparta II in the Gulf of Finland; corvette hit off Libya. | Reuters |
| 3 | Huawei guilty on 10 of 12 counts — US jury convicts Huawei of trade-secret theft and bank fraud; racketeering acquitted. | AP |
| 4 | Houthi drone hits Riyadh PIF tower — Saudi says attack wounds at least 11; second hit in under a week. | Reuters |
| 5 | NATO vows to defend space — Rutte says alliance will defend against space threats after Russian satellite reports. | BBC |
| 6 | Senegal back as AFCON champions — CAS upholds Senegal appeal on Tuesday; title restored after CAF stripped it in March. | Reuters |
| 7 | Korea scrambles jets as Russia nears — South Korea orders Ulleungdo residents to shelter as Russian jets enter defence zone. | Reuters |
| 8 | Israel kills Hamas security chief — Strike kills Brig. Gen. Naeem Abu Mohammed Nahel in Gaza; six others die. | Reuters |
| 9 | Dow tops 50,000 first time — Dow closes at 50,019, up 0.85%, as Nasdaq falls 1.5% and the S&P slips 0.5%. | AP |
| 10 | US drone helps catch El Chapo Isidro — Mexico says US drone helped capture cartel boss in Sinaloa; Mexico will try him. | AP |
| 11 | Solomons pick Australia as top partner — Solomon Islands names Australia primary security partner in treaty excluding China. | AP |
| 12 | IRGC says it hit ship in Hormuz — IRGC says its navy hit a ship that went dark. | AP |
| 13 | Houthis 60 km from Aden — Yemen army: Houthis near Aden, poised to attack. | Reuters |
| 14 | UK sanctions Houthis — UK freezes assets, bans travel for four officials. | Reuters |
| 15 | Iraq takes Kurdish oilfields — Baghdad takes control of fields; Barzani objects. | Reuters |
| 16 | Saudi strikes kill 25 in Yemen — Saudi jets hit buses in Lahj; 25 dead or missing. | Reuters |
| 17 | Gaza meningitis alert — Ministry reports 272 cases in October, 15 deaths. | Reuters |
| 18 | Turkish helicopter crash kills 5 — AS-532 crashes after takeoff from Eskisehir. | Reuters |
| 19 | Haftar visits Turkey — Libyan commander meets Erdogan in Ankara. | Reuters |
| 20 | Cartagena hostages held — Gunmen hold 25 hostage; five older women freed. | Reuters |
| 21 | Car bomb injures 23 in Colombia — Blast hits offices; president blames narco-terror. (Happened Monday night, first reported Tuesday.) | AP |
| 22 | Zelensky urges four-way talks — Kyiv ready to meet Russia, US, Europe on Tuesday. | Reuters |
| 23 | Putin admits fuel strain — Putin says Ukraine strikes burden the fuel market. | Reuters |
| 24 | Pentagon rebukes Canada — US says Ottawa falls short on defence, F-35 review. | Reuters |
| 25 | US blacklists Nvidia-linked firm — Megaspeed, six firms put on Entity List over chips. | Reuters |
| 26 | Malaysia to return migrants — Anwar: thousands to return, 1,500 by ship in Dec. | Reuters |
| 27 | Hasina plans December return — Hasina plans Dec 16 return; jail awaits, says govt. | Reuters |
| 28 | Indonesia picks VP candidates — Prabowo nominates Amran Sulaiman and Sugiono. | Reuters |
| 29 | Hanoi blast kills six — Hot pot blast in Dong Da; gas leak suspected. | Reuters |
| 30 | China sentences spy to death — Official gave 35 secrets to a foreign country. | Reuters |
| 31 | US loses measles-free status — US loses measles-free status after 25-plus years. | Reuters |
| 32 | US tariffs threat on China, EU — US may tariff China, EU over subsidies, AP says. | AP |
| 33 | North Korea expels Swiss diplomat — Pyongyang demands Swiss office in capital shut. | Reuters |
| 34 | Bukele names soldiers killed in Haiti — Three Salvadorans die in accidental blast in Haiti. | Reuters |
| 35 | Congo plane missing, rebels claim hit — DRC plane missing; rebels claim they shot it down. | Reuters |

**Key metrics (KPI bar):** Dow 50,019 • Nasdaq −1.5% • Huawei guilty 10/12 • Hormuz 4 tankers • Senegal AFCON back • Houthis 60 km from Aden.

## Verification performed

- Ran `python3 -P -s main.py` twice: both wrote `output/entry.png`, **46,425 bytes, 1024×1024, SHA-256 `36a20676f8796d843419353b163d44561a29b601bd387d20662ba5dfcdf153cb` — byte-identical**.
- Text-fit check (same wrap function as the renderer): hero headlines ≤3 lines, hero summaries ≤2 lines, medium headlines ≤3 lines, medium summaries ≤3 lines, digest headlines/details fit their 308 px columns, title 858 px in 992 px, KPI 677 px. No `...` truncation, no clipping found on visual inspection at full size.
- Layout: same Rank-1-style broadsheet as the Nov 23 entry (ranked 1,206th of 16,928): huge title, 3 hero cards, 8 medium cards, large map with 11 pins, 2-column digest, verification footer.
- Honest limit: the renderer is pure-stdlib with a hand-built 5×7 bitmap font, so there is no true anti-aliasing; the type is chunky pixel by design.

## Layout

Ivory `#FAF7F0` / navy `#101E33` / gold `#C69E36` broadsheet. Original flat-vector drawings (no photos, no copied artwork). `main.py` is the only program; `entry.png` is its output.
