# İlk Release Oluşturma

GitHub Actions workflow'u ekledikten sonra, ilk .exe'yi oluşturmak için:

## Otomatik (Tavsiye Edilen):

1. GitHub'da repository'ye git
2. **Actions** sekmesine tıkla
3. **"Build Windows EXE"** workflow'unu seç
4. **"Run workflow"** → **"Run workflow"** (yeşil buton)
5. Workflow tamamlanınca **"Artifacts"** bölümünden .exe'yi indir

## Manuel Release:

Repository'de:

```bash
git tag v1.0.0
git push origin v1.0.0
```

Bu otomatik olarak .exe oluşturacak ve Release'e ekleyecek!
