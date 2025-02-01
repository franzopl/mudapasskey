import qbittorrentapi
chaveantiga = "yyyyyyyyyyyyy" #escreva aqui a passkey antiga
chave = "xxxxxxxxxxxxxxxxxxx" #escreva aqui sua passkey nova
# API configuração
qb = qbittorrentapi.Client(host='0.0.0.0:8080', username='usuario', password='senhadificilcommuitasletras')


#A PARTIR DESTA LINHA VOCÊ NÃO PRECISA ALTERAR NADA

# nova URL
new_tracker_url = "https://capybarabr.com/announce/"+chave

# tenta logar no qBittorrent
try:
    qb.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(f"Erro de conexão: {e}")
    exit(1)

# Busca a lista de tidis is torrents
try:
    torrents = qb.torrents_info()
except qbittorrentapi.APIError as e:
    print(f"Erro ao localizar lista de torrents: {e}")
    qb.auth_log_out()
    exit(1)

# Inicia contadores
total_count = len(torrents)
changed_count = 0
ignored_count = 0

for torrent in torrents:
    try:
        print(f"Torrent: {torrent.name}")
        # Pega a lista de trackers para o torent atual
        trackers = qb.torrents_trackers(torrent.hash)
        for tracker in trackers:
            # Ignora outros trackers como  DHT, PeX, and LSD, se voce tiver muitos crossseed pode adicionar aqui para pular e acelerar um pouco o processo
            if tracker.url not in ['** [DHT] **', '** [PeX] **', '** [LSD] **']:
                if chaveantiga in tracker.url: 
                    if tracker.url != new_tracker_url:
                        # susbistui a URL antiga pela nova
                        qb.torrents_edit_tracker(torrent_hash=torrent.hash, original_url=tracker.url, new_url=new_tracker_url)
                        print(f"  Tracker antigo: {tracker.url} substituido por {new_tracker_url}")
                        changed_count += 1
                    else:
                        print(f"  Torrent ignorado pois já possui o mesmo tracker: {tracker.url}")
                        ignored_count += 1
                else:
                    print(f"  Tracker {tracker.url} não possui "+chave+", sem alterações.")
        print("-")
    except qbittorrentapi.APIError as e:
        print(f"Erro ao processar {torrent.name}: {e}")

# Apresenta resumo
print(f"Número total de torrents: {total_count}")
print(f"Número de trackers substituidos: {changed_count}")
print(f"Número de torrents ignorados: {ignored_count}")

# Log out do  qBittorrent
qb.auth_log_out()
