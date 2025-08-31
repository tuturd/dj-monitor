# DJ Monitor

Application web de monitoring et d’affichage en temps réel pour DJ, réalisée avec Flask et Socket.IO.

- Permet la configuration et la diffusion d’un message personnalisé (texte, couleur, mode clignotant).
- Affiche un compte à rebours (countdown) jusqu’à une date/heure cible, avec gestion d’alerte (warning).
- Interface de configuration accessible via `/config`, affichage principal via `/monitor`.
- Synchronisation instantanée des changements via WebSocket.
- Architecture modulaire et professionnelle : routes et sockets orientés objet, configuration persistante, support Docker/WSL.
- Accès possible depuis le réseau local (PC, tablette, smartphone).

Idéal pour la gestion d’annonces, de timing et d’alertes lors d’événements DJ ou tout autre contexte nécessitant un affichage dynamique et centralisé.

## WSL2 Configuration

Some configuration is required to make this service accessible when running under Docker on WSL2:

The WSL2 IP address can be found using the command `ip addr`

```bash
# Open TCP port 80 (on Windows Terminal)
New-NetFirewallRule -DisplayName "Allow TCP 80" -Direction Inbound -LocalPort 80 -Protocol TCP -Action Allow

# Port forwarding (on Windows Terminal)
netsh interface portproxy add v4tov4 listenport=80 listenaddress=0.0.0.0 connectport=8080 connectaddress=<ipWSL>
```

To remove these configurations:
```bash
# Close TCP port 80 (on Windows Terminal)
Remove-NetFirewallRule -DisplayName "Allow TCP 80"

# Remove port forwarding (on Windows Terminal)
netsh interface portproxy delete v4tov4 listenport=80 listenaddress=0.0.0.0
```

### Other Useful Commands

To display all existing portproxy rules:
```bash
netsh interface portproxy show all
```

To list open TCP ports on your system, use the following command:

```bash
netstat -an | findstr LISTEN
```

Or, for a more detailed view (on Linux):

```bash
sudo ss -tuln
```