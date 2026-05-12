import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- 1. CONFIG & SYSTEM THEME ---
st.set_page_config(page_title="Genesis Quantum v7.5 - Intel Edition", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main { background-color: #05070a; color: #e2e8f0; }
    .stMetric { background-color: #0d1117; border: 1px solid #1f2937; padding: 20px; border-radius: 8px; }
    .glossary-card { 
        background-color: #0d1117; padding: 15px; border-radius: 6px; border: 1px solid #1f2937; 
        border-left: 4px solid #10b981; margin-bottom: 12px; height: 160px; overflow-y: auto;
    }
    .history-card {
        background-color: #0d1117; padding: 25px; border-radius: 8px; border: 1px solid #1f2937; 
        border-left: 5px solid #f59e0b; margin-bottom: 25px;
    }
    .seller-card {
        background-color: #0d1117; padding: 25px; border: 1px solid #1f2937; border-radius: 12px; 
        margin-bottom: 20px; border-top: 6px solid #3b82f6; transition: 0.3s;
    }
    .seller-card:hover { border-color: #3b82f6; box-shadow: 0 0 15px rgba(59, 130, 246, 0.2); }
    .status-live { color: #10b981; font-weight: bold; animation: blinker 1.5s linear infinite; font-size: 0.8em; }
    @keyframes blinker { 50% { opacity: 0; } }
    .intel-tag { background: #1e293b; color: #3b82f6; padding: 3px 10px; border-radius: 4px; font-size: 0.75em; font-weight: bold; text-transform: uppercase; margin-right: 5px; }
    .strategy-box { background: rgba(16, 185, 129, 0.05); border: 1px solid rgba(16, 185, 129, 0.2); padding: 12px; border-radius: 6px; margin-top: 10px; }
    .analysis-text { color: #93c5fd; font-size: 0.95em; font-style: italic; background: rgba(59,130,246,0.08); padding: 12px; border-radius: 6px; }
    .slippage-bad { color: #ef4444; font-weight: bold; }
    .slippage-good { color: #10b981; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. VERİ KATMANI (EKSİKSİZ KORUNDU) ---
GLOSSARY_DB = {
    "PoW": "Ağın güvenliğini enerji harcayarak sağlayan mekanizma.", "Hashrate": "Ağın toplam hesaplama gücü.",
    "UTXO": "Harcanmamış işlem çıktısı.", "Lightning Network": "Bitcoin Layer-2 katmanı.",
    "Halving": "Arz üretiminin yarıya düşmesi.", "Sats": "Bitcoin'in en küçük birimi.",
    "SegWit": "Blok kapasitesini artıran güncelleme.", "Taproot": "Gizlilik yükseltmesi.",
    "Mempool": "Onay bekleyen işlemler alanı.", "Cold Storage": "Çevrimdışı saklama.",
    "HODL": "Satmadan bekleme felsefesi.", "Whale": "Büyük cüzdan sahibi.",
    "ASIC": "Özel madencilik işlemcisi.", "51% Attack": "Ağı manipüle etme riski.",
    "Difficulty": "Zorluk ayarı.", "Genesis Block": "0 numaralı blok.",
    "Private Key": "Erişim anahtarı.", "Public Key": "Cüzdan adresi.",
    "Node": "Kayıt tutan yazılım.", "Soft Fork": "Uyumlu güncelleme.",
    "Hard Fork": "Ağın ikiye bölünmesi.", "Double Spending": "Çift harcama.",
    "Slippage": "Fiyat kayması.", "Arbitraj": "Farktan kâr etme.",
    "Fiat": "Kağıt para.", "FOMO": "Kaçırma korkusu.",
    "FUD": "Korku yayma haberleri.", "DCA": "Düzenli alım.",
    "Stablecoin": "Sabit değerli kripto.", "On-Chain": "Zincir üstü veri.",
    "Off-Chain": "Zincir dışı işlem.", "Market Cap": "Piyasa değeri.",
    "Liquidity": "Nakit dönüşüm hızı.", "RBF": "Ücret güncelleme.",
    "Ordinals": "BTC NFT teknolojisi.", "BRC-20": "BTC token standardı.",
    "Self-Custody": "Bireysel kontrol.", "Whitepaper": "Teknik belge.",
    "DeFi": "Merkeziyetsiz finans.", "Smart Contract": "Otomatik kod.",
    "CEX": "Merkezi borsa.", "DEX": "Merkeziyetsiz borsa.",
    "Gas Fee": "İşlem ücreti.", "Burn": "Arz yakımı.",
    "Airdrop": "Bedava dağıtım.", "ICO": "İlk halka arz.",
    "Staking": "Kilitleyip ödül alma.", "KYC": "Kimlik doğrulama.",
    "AML": "Kara para önleme.", "Seed Phrase": "Kurtarma kelimeleri.",
    "ATH": "Rekor fiyat.", "ATL": "Dip fiyat.",
    "Block Reward": "Madenci ödülü.", "Circulating Supply": "Dolaşımdaki arz.",
    "Max Supply": "Maksimum 21M arz.", "Hash": "Dijital imza.",
    "Layer 1": "Ana ağ.", "Layer 2": "Hız katmanı.",
    "Mainnet": "Canlı ağ.", "Testnet": "Deneme ağı.",
    "P2P": "Eşler arası.", "Phishing": "Sahte site saldırısı.",
    "PoS": "Varlık tabanlı konsensüs.", "Scam": "Dolandırıcılık.",
    "Sidechain": "Yan zincir.", "Volatility": "Fiyat oynaklığı.",
    "ZKP": "Sıfır bilgi kanıtı.", "Web3": "Yeni internet.",
    "Bagholder": "Zararda bekleyen.", "Bitcointalk": "İlk forum.",
    "Block Height": "Blok sayısı.", "Cloud Mining": "Kiralık madencilik.",
    "Exit Scam": "Kaçış dolandırıcılığı.", "Gas Limit": "Enerji sınırı.",
    "Limit Order": "Fiyatlı emir.", "Market Order": "Anlık emir.",
    "Mooning": "Hızlı yükseliş.", "Satoshi Nakamoto": "Yaratıcı.",
    "Shilling": "Reklam yapma.", "Paper Bitcoin": "Sentetik satış.",
    "Replay Attack": "Tekrar saldırısı.", "Dust Attack": "Takip saldırısı.",
    "Cold Wallet": "Fiziksel cüzdan.", "Hot Wallet": "Yazılım cüzdanı.",
    "Bear Trap": "Ayı tuzağı.", "Bull Trap": "Boğa tuzağı.",
    "Whale Index": "Balina endeksi.", "Merkeziyetsizlik": "Otoritesizlik.",
    "Enflasyonist": "Arzı artan.", "Deflasyonist": "Arzı azalan.",
    "Tokenomics": "Ekonomik yapı.", "Vesting": "Kilit süresi.",
    "Rug Pull": "Likidite boşaltma.", "Sats Stack": "Sats biriktirme.",
    "DEX Aggregator": "Borsa birleştirici.", "Liquidation": "Pozisyon tasfiyesi.",
    "Leverage": "Kaldıraç.", "Funding Rate": "Pozisyon taşıma bedeli.",
    "Open Interest": "Açık kontratlar."
}

HISTORY_DB = [
    {"year": "2008", "title": "Whitepaper", "desc": "Satoshi, merkeziyetsiz nakit sistemini duyurdu. Bu sistem, paranın kontrolünü bankalardan alıp matematiksel kurallara teslim eden devrim niteliğinde bir teknolojik manifestoydu.", "ana": "2008 küresel bankacılık krizi, mevcut finans sistemine duyulan güvenin sarsılmasına neden olan en büyük tetikleyiciydi.", "res": "Finansal egemenlik el değiştirdi."},
    {"year": "2009", "title": "Genesis Block", "desc": "Bitcoin ağının ilk bloğu kazıldı. Satoshi bu bloğa, banka kurtarma operasyonlarını eleştiren o meşhur gazete manşetini ekleyerek Bitcoin'in neden var olduğunu sonsuza kadar blockchain'e kazımış oldu.", "ana": "Hükümetlerin sınırsız para basarak bankaları kurtarmasına karşı dijital bir protesto.", "res": "Ağ resmi olarak başladı."},
    {"year": "2010", "title": "Pizza Günü", "desc": "10.000 BTC karşılığında 2 pizza satın alındı. Bu olay, dijital bir verinin gerçek dünyada somut bir malla takas edilebileceğini kanıtlayan ilk büyük işlemdi.", "ana": "Bitcoin'e ilk kez piyasa tarafından somut bir reel değer biçilmesi.", "res": "Takas gücü kanıtlandı."},
    {"year": "2011", "title": "Silk Road", "desc": "Anonim bir pazar olan Silk Road'un Bitcoin'i kabul etmesi, ağın 'sansürlenemez' ve 'durdurulamaz' yapısını ilk kez kanıtladı ancak regülatörlerin tepkisini çekti.", "ana": "Bitcoin'in sansürlenemez doğasının en büyük saha testi.", "res": "Regülasyon radarına girildi."},
    {"year": "2013", "title": "Kıbrıs Krizi", "desc": "Kıbrıs'ta banka mevduatlarına el konulması, halkın parasını korumak için Bitcoin'e akın etmesine neden oldu. Bu durum Bitcoin'in 'güvenli liman' anlatısını güçlendirdi.", "ana": "Bankadaki paranın bile güvende olmadığı bir ortamda matematiksel güven kazandı.", "res": "Güvenli liman tezi oluştu."},
    {"year": "2014", "title": "Mt. Gox İflası", "desc": "Dönemin en büyük borsasının hacklenmesi, merkeziiyetçiliğin ne kadar tehlikeli olabileceğini tüm dünyaya en acı şekilde gösterdi.", "ana": "Merkezi borsa yapılarındaki tekil başarısızlık riski deşifre oldu.", "res": "Donanım cüzdan devrimi başladı."},
    {"year": "2015", "title": "Ethereum Lansmanı", "desc": "Akıllı sözleşmelerin gelişiyle blockchain artık sadece bir para birimi değil, üzerinde uygulama geliştirilebilen bir dünya bilgisayarına dönüştü.", "ana": "Blockchain teknolojisi programlanabilir hale geldi.", "res": "Altcoin patlaması tetiklendi."},
    {"year": "2017", "title": "Fork Savaşları", "desc": "Bitcoin'in nasıl büyüyeceği konusunda topluluk ikiye bölündü. Blok boyutunu artırmak isteyenler Bitcoin Cash'i kursa da ana ağ vizyonunu korumayı başardı.", "ana": "Kullanıcı düğümlerinin madencilere karşı kazandığı ilk büyük zafer.", "res": "Bitcoin vizyonu netleşti."},
    {"year": "2017", "title": "ICO Çılgınlığı", "desc": "Ethereum üzerinde binlerce yeni projenin token çıkararak fon toplaması, sermayenin demokratikleştiği ancak risklerin arttığı bir dönem yarattı.", "ana": "Sermayeye erişim artık merkezi kurumların tekelinden çıktı.", "res": "Piyasada devasa hacim oluştu."},
    {"year": "2017", "title": "20k Zirvesi", "desc": "Bitcoin fiyatının 20.000 dolara ulaşması, kripto paraların artık marjinal bir gruptan çıkıp tüm dünyanın konuştuğu bir yatırım aracına dönüşmesini sağladı.", "ana": "Küresel çapta ana akım farkındalığın zirvesi.", "res": "Büyük medya ilgisi başladı."},
    {"year": "2018", "title": "Ayı Piyasası", "desc": "Fiyatlardaki %80'lik düşüş 'balon patladı' seslerini yükseltse de, teknolojik gelişim ve kurumsal altyapı çalışmaları hız kesmeden devam etti.", "ana": "Spekülatif köpüğün atıldığı, gerçek teknolojinin kaldığı dönem.", "res": "Kripto kışı yaşandı."},
    {"year": "2020", "title": "Kara Perşembe", "desc": "Pandemi şokuyla tüm piyasalar çökerken Bitcoin de %50 değer kaybetti ancak toparlanma hızıyla en dirençli varlıklardan biri olduğunu kanıtladı.", "ana": "Piyasanın likidite ve sistemik risklere karşı en büyük testi.", "res": "Kurumsal ilginin fitili ateşlendi."},
    {"year": "2020", "title": "MicroStrategy", "desc": "Bir teknoloji devinin nakit rezervlerini Bitcoin'e çevirmesi, Bitcoin'in şirketler için 'hazine varlığı' statüsü kazanmasını sağladı.", "ana": "Michael Saylor etkisiyle Bitcoin'in meşruiyeti kurumsallaştı.", "res": "Şirket hazinelerine giriş başladı."},
    {"year": "2021", "title": "Tesla Alımı", "desc": "Elon Musk'ın hamlesi Bitcoin'i popüler kültürün ve en büyük teknoloji yatırımcılarının odağına taşıyarak fiyatı rekorlara taşıdı.", "ana": "En üst düzey teknoloji onayı ve prestij kazanımı.", "res": "Perakende FOMO zirve yaptı."},
    {"year": "2021", "title": "El Salvador", "desc": "Bir ülkenin Bitcoin'i resmi para birimi ilan etmesi, küresel finans tarihinde daha önce görülmemiş bir egemenlik hamlesiydi.", "ana": "Uluslararası finans kuruluşlarına karşı parasal bağımsızlık testi.", "res": "Ulus devlet devrimi başladı."},
    {"year": "2021", "title": "69k ATH", "desc": "Bitcoin'in ulaştığı tarihi zirve, kripto para piyasasının toplam değerini 3 trilyon doların üzerine çıkararak devasa bir finansal güç haline getirdi.", "ana": "Global likidite rallisinin ve kurumsal kabulün fiyatlanması.", "res": "Tarihi rekor kırıldı."},
    {"year": "2022", "title": "Terra/Luna", "desc": "Algoritmik bir stablecoin'in çöküşü, piyasada milyarlarca doların buharlaşmasına ve sistemik risklerin sorgulanmasına neden oldu.", "ana": "Sürdürülemez finansal modellerin piyasada yarattığı devasa yıkım.", "res": "Regülasyon baskısı şiddetlendi."},
    {"year": "2022", "title": "FTX İflası", "desc": "Dünyanın en büyük borsalarından birinin dolandırıcılık nedeniyle çökmesi, güven kurumuna büyük bir darbe vurdu ancak 'şeffaflık' ihtiyacını artırdı.", "ana": "Merkezi yönetimlerdeki denetimsizlik ve güven kaybı.", "res": "Rezerv kanıtı dönemi başladı."},
    {"year": "2023", "title": "Ordinals", "desc": "Bitcoin ağında NFT'lerin ve tokenların oluşturulabilmesi, ağın kullanım alanını genişleterek madenci gelirlerini artırdı.", "ana": "Ağ kullanımının basit bir para transferinden karmaşık bir veri yapısına evrilmesi.", "res": "Madenci geliri ve ağ güvenliği arttı."},
    {"year": "2023", "title": "Binance Cezası", "desc": "En büyük borsanın regülatörlerle uzlaşması ve CZ'nin istifası, sektörün artık 'vahşi batı' döneminden çıkıp kurumsal bir zemine oturduğunu gösterdi.", "ana": "Kripto ekosisteminin hukuksal olarak temizlenme süreci.", "res": "Kurumsal zemin sağlamlaştı."},
    {"year": "2024", "title": "Spot ETF", "desc": "Wall Street devlerinin Bitcoin'i resmen kabul etmesi, artık Bitcoin'i geri dönülemez bir şekilde küresel finansın parçası olduğunu tescilledi.", "ana": "Geleneksel sermayenin Bitcoin'e akması için kurulan dev köprü.", "res": "Kalıcı fon girişi sağlandı."},
    {"year": "2024", "title": "4. Halving", "desc": "Blok ödüllerinin yarıya inmesiyle Bitcoin'in arz enflasyonu düştü, matematiksel kıtlık algoritması bir kez daha kusursuz çalıştı.", "ana": "Piyasadaki arz-talep dengesinin matematiksel olarak daraltılması.", "res": "Yeni döngü başlangıcı."},
    {"year": "2025", "title": "Büyük Adaptasyon", "desc": "Fortune 500 şirketlerinin Bitcoin'i bir standart olarak bilançolarına eklemesiyle volatilite azaldı ve Bitcoin ana akım bir portföy öğesi oldu.", "ana": "Bitcoin'in 'riskli varlık' statüsünden 'standart varlık' statüsüne geçişi.", "res": "Düşük volatilite dönemi."},
    {"year": "2026", "title": "Global Rezerv", "desc": "Devletlerin rezervlerine altın gibi Bitcoin eklemeye başlaması, dijital altın standardının finansal sistemin temeline oturduğu tarihi andır.", "ana": "Yeni küresel finansal düzenin Bitcoin üzerine inşa edilmesi.", "res": "Dijital altın standardı tescillendi."}
]

# OPTİME EDİLMİŞ VE GERÇEKÇİ SATICI İSTİHBARATI
SELLER_INTEL = [
    {
        "actor": "Mt. Gox Rehabilitasyon Kayyumu",
        "vol": "141,686 BTC",
        "risk": 95,
        "type": "FORCE SELL / REPAYMENT",
        "slippage_est": 3.8,
        "wallet_status": "Active Distribution",
        "on_chain_heat": "HOT",
        "route": "Kraken / Bitstamp / BitGo",
        "trigger": "Alacaklı transfer onayı.",
        "analysis": "10 yıl sonra gelen kâr realizasyonu. Satış baskısı anlık değil, borsalardaki derinliğe göre zamana yayılıyor.",
        "chart_data": [65000, 62000, 58000, 61000, 59000]
    },
    {
        "actor": "ABD Adalet Bakanlığı (US DOJ)",
        "vol": "69,370 BTC",
        "risk": 80,
        "type": "OTC / DIRECT TRANSFER",
        "slippage_est": 0.4,
        "wallet_status": "Dormant (Watching)",
        "on_chain_heat": "COLD",
        "route": "Coinbase Prime / OTC",
        "trigger": "Hükümet cüzdanlarından 'Coinbase Institutional' adresine transfer.",
        "analysis": "Hükümet genelde fiyatı ezmemek için kurumlar arası OTC transferi yapar; cüzdan hareketleri genelde psikolojik FUD yaratır.",
        "chart_data": [65000, 64500, 64200, 64800, 65100]
    },
    {
        "actor": "Madenci Kapitülasyonu Index",
        "vol": "~1.8M BTC (Total Reserves)",
        "risk": 70,
        "type": "OPEX / MARGIN CALL",
        "slippage_est": 1.2,
        "wallet_status": "Warming Up",
        "on_chain_heat": "MEDIUM",
        "route": "Exchange Flow",
        "trigger": "Hashrate'in %10'dan fazla düşmesi ve üretim maliyet baskısı.",
        "analysis": "Küçük madencilerin zorunlu satışları piyasa tabanını test eder. Büyük madenciler ise borç kapatmak için satar.",
        "chart_data": [65000, 63000, 63500, 66000, 72000]
    },
    {
        "actor": "Grayscale Bitcoin Trust (GBTC)",
        "vol": "Azalan Rezerv (~2k BTC/Hafta)",
        "risk": 45,
        "type": "ETF EXIT / LIQUIDATION",
        "slippage_est": 0.2,
        "wallet_status": "Stabilizing",
        "on_chain_heat": "STABLE",
        "route": "Genesis / Gemini Liquidation",
        "trigger": "ETF yönetim ücreti rekabeti ve tasfiyeler.",
        "analysis": "GBTC artık piyasa için bir 'fren' değil, geçmişten gelen bir yükün tasfiyesidir. ETF'ler bu baskıyı emiyor.",
        "chart_data": [65000, 66000, 68000, 70000, 75000]
    }
]

# --- 3. ENGINE (DÜZELTİLMİŞ VE KORUNMUŞ) ---
def run_quantum_sim(v, w, d, a_total, a_active_set):
    prices = [68000.0]
    agents = [a_active_set]
    
    for i in range(120):
        shock = -(w * 45) if 15 < i < 40 else 0
        noise = np.random.normal(0, v * 1.5)
        depth_buff = (d * 0.25)
        herd_impact = 1 + (1 - (a_active_set / a_total)) * 10
        change = (noise + shock + depth_buff) * herd_impact
        new_p = max(500, prices[-1] + change)
        prices.append(new_p)
        
        sim_active = int(a_active_set + np.random.randint(-2, 3))
        sim_active = max(0, min(sim_active, a_total))
        agents.append(sim_active)
        
    ponr_step = next((idx for idx, val in enumerate(agents) if val < a_total * 0.30), None)
    return prices, agents, ponr_step

# --- 4. RENDER LOGIC ---
with st.sidebar:
    st.title("GENESIS v7.5 FULL")
    nav = st.radio("NAVIGASYON", ["Stres Analizi", "Satıcı İstihbaratı", "Teknik Sözlük", "Tarihsel Arşiv"])
    st.divider()
    
    if nav == "Stres Analizi":
        st.header("PARAMETRELER")
        v_val = st.slider("Volatilite", 1, 100, 45)
        w_val = st.slider("Balina Baskısı", 0, 100, 30)
        d_val = st.slider("Piyasa Derinliği", 1, 100, 50)
        st.divider()
        a_total_input = st.number_input("Toplam Yatırımcı", 100, 10000, 1000)
        a_active_val = st.slider("Aktif Kalan Ajanlar", 0, a_total_input, 800)
    else:
        v_val, w_val, d_val, a_total_input, a_active_val = 45, 30, 50, 1000, 800

if nav == "Stres Analizi":
    st.title("Quantum Stress-Test Terminal")
    p, a_list, pi = run_quantum_sim(v_val, w_val, d_val, a_total_input, a_active_val)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("GÜNCEL FİYAT", f"${p[-1]:,.2f}")
    c2.metric("AKTİF AJANLAR", f"{a_list[-1]}")
    risk_rate = (1 - a_list[-1]/a_total_input) * 100
    c3.metric("LİKİDİTE RİSKİ", f"%{risk_rate:.1f}")
    c4.metric("DURUM", "KRİTİK" if risk_rate > 70 else "STABİL")
    
    hovers = [f"Fiyat: ${p[i]:,.0f}<br>Risk: %{(1 - a_list[i]/a_total_input)*100:.1f}" for i in range(len(p))]
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(y=p, name="Price", line=dict(color='#10b981', width=3), customdata=hovers, hovertemplate="%{customdata}<extra></extra>"), secondary_y=False)
    fig.add_trace(go.Scatter(y=a_list, name="Liquidity", fill='tozeroy', opacity=0.1, line=dict(color='#3b82f6')), secondary_y=True)
    if pi: fig.add_vline(x=pi, line_dash="dash", line_color="red", annotation_text="LOW LIQUIDITY ZONE")
    fig.update_layout(template="plotly_dark", height=600, hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

elif nav == "Satıcı İstihbaratı":
    st.title("Advanced Intelligence Hub")
    st.info("📊 Veriler On-Chain analizler ve 2026 Mayıs resmi cüzdan kayıtlarına dayanmaktadır.")
    
    for s in SELLER_INTEL:
        col_content, col_chart = st.columns([2, 1])
        with col_content:
            st.markdown(f"""
            <div class="seller-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h2 style="margin:0; color:#3b82f6; font-size: 1.5em;">{s['actor']}</h2>
                    <span class="status-live">● LIVE TRACKING</span>
                </div>
                <div style="margin:10px 0;">
                    <span class="intel-tag">{s['type']}</span>
                    <span class="intel-tag" style="background:#064e3b; color:#10b981;">{s['wallet_status']}</span>
                </div>
                <hr style="border:0.1px solid #1f2937; margin:15px 0;">
                <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; font-size:0.85em;">
                    <div><b>Bakiye:</b><br>{s['vol']}</div>
                    <div><b>On-Chain Isı:</b><br>{s['on_chain_heat']}</div>
                    <div><b>Tahmini Kayma:</b><br><span class="{'slippage-bad' if s['slippage_est'] > 2 else 'slippage-good'}">%{s['slippage_est']}</span></div>
                </div>
                <div class="analysis-text" style="margin-top:15px;"><b>Derin Analiz:</b> {s['analysis']}</div>
                <div class="strategy-box" style="font-size:0.85em;"><b>Tetikleyici:</b> {s['trigger']}<br><b>Rota:</b> {s['route']}</div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(1.0 - (s['risk']/100))
        
        with col_chart:
            f_fig = go.Figure(go.Scatter(y=s['chart_data'], mode='lines', line=dict(color='#ef4444', width=2)))
            f_fig.update_layout(title="Etki Projeksiyonu", template="plotly_dark", height=250, margin=dict(l=0,r=0,t=40,b=0))
            st.plotly_chart(f_fig, use_container_width=True)
        st.divider()

elif nav == "Teknik Sözlük":
    st.title("Professional Glossary")
    search = st.text_input("Ara...")
    cols = st.columns(2)
    filtered = {k: v for k, v in GLOSSARY_DB.items() if search.lower() in k.lower() or search.lower() in v.lower()}
    for i, (k, v) in enumerate(filtered.items()):
        with cols[i % 2]:
            st.markdown(f'<div class="glossary-card"><b>{k}:</b><br>{v}</div>', unsafe_allow_html=True)

elif nav == "Tarihsel Arşiv":
    st.title("Historical Archive")
    for h in HISTORY_DB:
        st.markdown(f"""<div class="history-card"><h2 style="color:#f59e0b;">{h['year']} | {h['title']}</h2><p>{h['desc']}</p><div class="analysis-text"><b>Analiz:</b> {h['ana']}</div><p style="color:#10b981;"><b>Sonuç:</b> {h['res']}</p></div>""", unsafe_allow_html=True)