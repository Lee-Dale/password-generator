# password-generator 
# password-generator

## Was macht das Projekt?

Das Projekt erzeugt zufällige und sichere Passwörter mit Python. Jedes Passwort hat mindestens 4 Kleinbuchstaben, 4 Großbuchstaben und 4 Ziffern. Erlaubt sind außerdem die Zeichen `-` und `_`. Das Projekt benutzt das Modul `secrets`, weil es für sichere Zufallswerte gemacht ist.

Beispiel:

```python
from src.generator import generate_password

print(generate_password())      # 20 Zeichen (Standard)
print(generate_password(32))    # 32 Zeichen
```

Die Länge muss mindestens 12 sein. Sonst gibt die Funktion einen `ValueError`.

## Pipeline im Überblick

Die Pipeline ist in der Datei `.github/workflows/pipeline.yml`. Sie hat drei Jobs. Sie laufen nacheinander.

| Job | Was macht er? | Braucht (`needs`) |
|---|---|---|
| `test` | Installiert die Pakete und startet die Tests mit `python -m pytest -v`. Er benutzt einen Cache für pip. | nichts |
| `build` | Packt den Ordner `src/` in die Datei `build/app.zip`. Danach lädt er sie als Artifact `app-package` hoch. | `test` |
| `deploy` | Lädt das Artifact herunter, prüft das Secret und erstellt ein Release mit `app.zip`. | `build` |

Wenn ein Job fehlschlägt, starten die nächsten Jobs nicht.

Das Paket wird nur einmal gebaut (im Job `build`). Der Job `deploy` benutzt dasselbe Paket und baut nichts neu.

## Trigger

Die Pipeline startet bei:

- jedem `push` (auf jedem Branch)
- jedem `pull_request`

Die Jobs `test` und `build` laufen immer. Der Job `deploy` läuft **nur bei einem Push auf `main`**. Bei einem Pull Request wird er übersprungen. Das steuert diese Bedingung:

```yaml
if: github.ref == 'refs/heads/main'
```

## Secrets und Environment

**Secret** (nur der Name, nie der Wert):

- `DEPLOY_TOKEN`: wird im Job `deploy` benutzt. Im Log steht nur die Länge, nie der Wert.

**Variable:**

- `DEPLOY_TARGET`: das Ziel des Deployments (zum Beispiel `staging`)

**Automatisches Token:**

- `GITHUB_TOKEN`: wird von GitHub selbst gegeben. Es wird für das Release benutzt.

**Environment `production`:**

- Schutzregel: **Required reviewers**. Das Deployment wartet, bis eine Person es freigibt.
- Deployment-Branch: nur `main`

**Rechte (`permissions`):**

- Für alle Jobs: `contents: read` (nur lesen)
- Nur für `deploy`: zusätzlich `contents: write` (für das Release) und `actions: read` (für das Artifact)

## Deployment

Nach einem Push auf `main` passiert Folgendes:

1. `test` und `build` laufen und müssen grün sein.
2. Der Job `deploy` wartet auf die Freigabe. Im Tab **Actions** klickst du auf **Review deployments** und gibst `production` frei.
3. Danach erstellt die Pipeline automatisch ein Release mit dem Namen `v1.0.<Run-Nummer>`. Die Datei `app.zip` ist als Asset angehängt.

So prüfst du das Deployment:

- Öffne die Seite **Releases** im Repository: <https://github.com/Lee-Dale/password-generator/releases>
- Öffne das neueste Release und klappe **Assets** auf. Dort muss `app.zip` stehen.

## Lokal ausführen

```bash
# 1. Repository klonen
git clone https://github.com/Lee-Dale/password-generator.git
cd password-generator

# 2. Virtuelle Umgebung erstellen und starten
python3 -m venv .venv
source .venv/bin/activate

# 3. Pakete installieren
python -m pip install -r requirements.txt

# 4. Tests starten
python -m pytest -v

# 5. Paket bauen
mkdir -p build
python -m zipfile -c build/app.zip src/
```