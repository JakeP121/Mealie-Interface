# Mealie-Interface
Exposes Mealie API hooks to Home Assistant to be called by services

## Installation
### Option A (HACS)
- Go to HACS > Integration.
- Click the three dots in the upper right corner and click 'Custom Repositories'.
- Add https://github.com/JakeP121/Mealie-Interface to your repositories.
- Mealie Interface should now show up on your HACS integration page, click it and click download.
- Restart Home Assistant.
### Option B (Manual Installation
- Copy everything in https://github.com/JakeP121/Mealie-Interface/tree/main/custom_components/ to your \<config\>/custom_components/ folder
- Restart Home Assistant.

## Enabling
- Add the following to your \<config\>/configuration.yaml
```
  mealie_interface:
    username: <your_mealie_username>
    password: !secret mealie_password
    url: <your_mealie_url>
```
- Add the following to your \<config\>/secrets.yaml
```
mealie_password: <your_mealie_password>
```

