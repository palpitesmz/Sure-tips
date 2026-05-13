import requests
import json
import random
import string
import os
from datetime import datetime, timedelta

API_KEY = os.environ.get("API_KEY")
API_URL = "https://v3.football.api-sports.io"
HEADERS = {"x-apisports-key": API_KEY}

MERCADOS = {
    "over1.5": {"bet": 5, "value": "Over 1.5"},
    "btts": {"bet": 8, "value": "Yes"},
    "1x2": {"bet": 1, "value": "Home"} # Vamos pegar todas as 3 opções e escolher a melhor
}

def gerar_senha(tamanho=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=tamanho))

def buscar_jogos():
    hoje = datetime.now().strftime("%Y-%m-%d")
    ontem = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    url = f"{API_URL}/fixtures"
    params = {"date": hoje, "timezone": "Africa/Maputo", "status": "NS"}
    r = requests.get(url, headers=HEADERS, params=params)
    jogos_hoje = r.json().get("response", [])

    params = {"date": ontem, "timezone": "Africa/Maputo", "status": "FT"}
    r = requests.get(url, headers=HEADERS, params=params)
    jogos_ontem = r.json().get("response", [])

    return jogos_hoje, jogos_ontem

def pegar_melhor_palpite(odds_data, min_odd, max_odd):
    if not odds_data or "bookmakers" not in odds_data[0]:
        return None

    for bookmaker in odds_data[0]["bookmakers"]:
        for bet in bookmaker["bets"]:
            bet_name = bet["name"].lower()

            # Over 1.5
            if "over/under" in bet_name or "goals over/under" in bet_name:
                for value in bet["values"]:
                    if value["value"] == "Over 1.5":
                        odd = float(value["odd"])
                        if min_odd <= odd <= max_odd:
                            return {"palpite": "Mais de 1.5", "odd": str(odd)}

            # Ambas Marcam
            if "both teams to score" in bet_name:
                for value in bet["values"]:
                    if value["value"] == "Yes":
                        odd = float(value["odd"])
                        if min_odd <= odd <= max_odd:
                            return {"palpite": "Ambas Marcam", "odd": str(odd)}

            # 1X2
            if bet_name == "match winner" or bet_name == "1x2":
                melhor = None
                for value in bet["values"]:
                    try:
                        odd = float(value["odd"])
                        if min_odd <= odd <= max_odd:
                            if melhor is None or odd > float(melhor["odd"]):
                                melhor = {"palpite": value["value"], "odd": str(odd)}
                    except:
                        continue
                if melhor:
                    return melhor
    return None

def filtrar_palpites(jogos, min_odd, max_odd, limite):
    palpites = []
    count = 0

    for jogo in jogos:
        if count >= limite:
            break

        fixture_id = jogo["fixture"]["id"]

        url = f"{API_URL}/odds"
        params = {"fixture": fixture_id}
        try:
            r = requests.get(url, headers=HEADERS, params=params, timeout=10)
            odds_data = r.json().get("response", [])
        except:
            continue

        melhor = pegar_melhor_palpite(odds_data, min_odd, max_odd)
        if melhor:
            palpites.append({
                "jogo": f"{jogo['teams']['home']['name']} vs {jogo['teams']['away']['name']}",
                "palpite": melhor["palpite"],
                "odd": melhor["odd"],
                "liga": jogo["league"]["name"],
                "hora": jogo["fixture"]["date"][11:16]
            })
            count += 1

    return palpites

def filtrar_resultados(jogos):
    resultados = []
    for jogo in jogos:
        if jogo["fixture"]["status"]["short"] == "FT":
            total_gols = jogo["goals"]["home"] + jogo["goals"]["away"]
            status = "Green" if total_gols > 1 else "Red"
            resultados.append({
                "jogo": f"{jogo['teams']['home']['name']} vs {jogo['teams']['away']['name']}",
                "resultado": f"{jogo['goals']['home']}-{jogo['goals']['away']}",
                "status": status
            })
    return resultados

def main():
    jogos_hoje, jogos_ontem = buscar_jogos()

    # Grátis: 1.50 - 1.80, máx 2 jogos
    gratis = filtrar_palpites(jogos_hoje, 1.50, 1.80, 2)

    # VIP Diário: 2.00 - 3.00, máx 3 jogos
    vip_diario = filtrar_palpites(jogos_hoje, 2.00, 3.00, 3)

    # VIP Semanal: 3.00 - 4.00, máx 6 jogos
    vip_semanal = filtrar_palpites(jogos_hoje, 3.00, 4.00, 6)

    resultados = filtrar_resultados(jogos_ontem)

    senha_diario = gerar_senha()
    senha_semanal = gerar_senha()

    dados = {
        "senha_vip_diario": senha_diario,
        "senha_vip_semanal": senha_semanal,
        "palpites_gratis": gratis,
        "palpites_vip_diario": vip_diario,
        "palpites_vip_semanal": vip_semanal,
        "resultados_ontem": resultados,
        "ultima_atualizacao": datetime.now().strftime("%d/%m/%Y %H:%M")
    }

    with open("dados.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    print("Atualizado com sucesso!")
    print(f"Grátis: {len(gratis)} jogos")
    print(f"VIP Diário: {len(vip_diario)} jogos")
    print(f"VIP Semanal: {len(vip_semanal)} jogos")
    print(f"Senha VIP Diário: {senha_diario}")
    print(f"Senha VIP Semanal: {senha_semanal}")

if __name__ == "__main__":
    main()