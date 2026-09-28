import streamlit as st
import streamlit.components.v1 as components
import math
import datetime
import html
import json
import joblib
from pathlib import Path
from urllib.parse import quote
@st.cache_resource
def load_yield_model():
   return joblib.load("ml_models/yield_model.pkl")

yield_model = load_yield_model()

try:
    import requests
except ImportError:
    requests = None

try:
    import pandas as pd
except ImportError:
    pd = None
# ============================================================
# GRAM SAHAYAK
# Business & Financial Guidance for Rural Micro-Entrepreneurs
# ============================================================

st.set_page_config(
    page_title="Gram Sahayak",
    page_icon="🌾",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
:root {
  --gs-green:#2E7D32;
  --gs-green-dark:#1B5E20;
  --gs-mint:#E8F5E9;
  --gs-slate:#374151;
  --gs-muted:#6B7280;
  --gs-border:rgba(46,125,50,.18);
  --gs-card:#FFFFFF;
  --gs-bg:#F6FAF7;
}
.stApp{background:linear-gradient(180deg,#F8FBF8 0%,#F4F8F5 100%);color:var(--gs-slate);}
[data-theme="dark"] .stApp{background:#0e1510;color:#E5E7EB;}
.block-container{padding-top:1.5rem;padding-bottom:3rem;max-width:1480px;}
.hero{padding:1.7rem 1.9rem;border-radius:18px;background:linear-gradient(135deg,var(--gs-mint),#FFFFFF);border:1px solid var(--gs-border);margin-bottom:1.3rem;box-shadow:0 8px 24px rgba(27,94,32,.08);}
.hero h1{font-size:2.55rem;margin-bottom:.25rem;color:var(--gs-green-dark);}
.hero p{font-size:1.05rem;color:var(--gs-muted);line-height:1.6;}
.gs-card,.gs-metric,.gs-phase,.gs-scheme,.gs-table-wrap{border-radius:12px;border:1px solid var(--gs-border);box-shadow:0 4px 6px -1px rgba(0,0,0,.10),0 8px 18px rgba(27,94,32,.045);}
.gs-card{background:var(--gs-card);padding:20px;margin:.55rem 0 1rem;}
.gs-table-wrap{background:var(--gs-card);padding:12px 14px;margin:.6rem 0 1rem;overflow-x:auto;}
[data-theme="dark"] .gs-card,[data-theme="dark"] .gs-metric,[data-theme="dark"] .gs-phase,[data-theme="dark"] .gs-scheme,[data-theme="dark"] .gs-table-wrap{background:#141c16;border-color:rgba(144,202,149,.20);}
.gs-section-title{color:var(--gs-green-dark);font-weight:800;font-size:1.10rem;margin:.1rem 0 .4rem;}
.gs-microcopy{color:var(--gs-muted);font-size:.84rem;line-height:1.45;margin-bottom:.6rem;}
.gs-stepper{display:flex;gap:8px;flex-wrap:wrap;margin:.3rem 0 1.1rem;}
.gs-step{padding:7px 12px;border-radius:999px;border:1px solid var(--gs-border);background:#fff;font-size:.84rem;font-weight:700;color:#49604d;}
.gs-step.active{background:var(--gs-green);color:#fff;border-color:var(--gs-green);}
.gs-metric{background:linear-gradient(135deg,#F4FBF5,#FFFFFF);padding:16px 17px;min-height:106px;}
.gs-metric .label{font-size:.75rem;color:var(--gs-muted);text-transform:uppercase;letter-spacing:.05em;font-weight:750;}
.gs-metric .value{font-size:1.55rem;font-weight:850;color:var(--gs-green-dark);margin-top:4px;}
.gs-metric .hint{font-size:.78rem;color:var(--gs-muted);margin-top:5px;}
.gs-phase{padding:17px 18px;background:linear-gradient(135deg,rgba(232,245,233,.82),#fff);height:100%;}
.gs-phase .phase-no{display:inline-block;background:var(--gs-green);color:#fff;padding:4px 9px;border-radius:999px;font-size:.74rem;font-weight:800;margin-bottom:8px;}
.gs-risk-high{border-left:5px solid #C62828!important}.gs-risk-medium{border-left:5px solid #EF8B00!important}.gs-risk-low{border-left:5px solid #2E7D32!important}
.gs-scheme{padding:15px;background:linear-gradient(135deg,#F1F8F2,#FFFFFF);margin-bottom:12px;}
.gs-table{width:100%;border-collapse:collapse;font-size:.92rem;}
.gs-table th{background:var(--gs-green);color:#fff;text-align:left;padding:10px 11px;white-space:nowrap;}
.gs-table td{padding:9px 11px;border-bottom:1px solid rgba(107,114,128,.16);vertical-align:top;line-height:1.45;}
.gs-table tr:nth-child(even) td{background:rgba(232,245,233,.34);}
[data-theme="dark"] .gs-table tr:nth-child(even) td{background:rgba(46,125,50,.09);}
[data-theme="dark"] .gs-table td{border-bottom-color:rgba(229,231,235,.12);}
.gs-insight{padding:.85rem 1rem;border-radius:10px;background:var(--gs-mint);border-left:4px solid var(--gs-green);margin:.6rem 0;}
.gs-alert-note{font-size:.82rem;color:var(--gs-muted);}
.stExpander{border:1px solid var(--gs-border)!important;border-radius:12px!important;background:rgba(255,255,255,.72)!important;box-shadow:0 4px 6px -1px rgba(0,0,0,.06)!important;}
[data-theme="dark"] .stExpander{background:#121a15!important;}
div[data-baseweb="select"]>div,div[data-baseweb="input"]>div,textarea{border-radius:10px!important;}
input,textarea{line-height:1.4!important;}
button[kind="primary"]{background:var(--gs-green)!important;border-color:var(--gs-green)!important;}
button[kind="primary"]:hover{background:var(--gs-green-dark)!important;border-color:var(--gs-green-dark)!important;}
.footer{text-align:center;color:var(--gs-muted);padding:2rem 0 .5rem;}
.small-note{color:var(--gs-muted);font-size:.86rem;}

.gs-roadmap-wrap{position:relative}.gs-roadmap-card{background:#fff;border:1px solid var(--gs-border);border-left:5px solid var(--gs-green);border-radius:16px;padding:18px 20px;margin:6px 0;box-shadow:0 6px 18px rgba(46,125,50,.08)}.gs-roadmap-top{display:flex;align-items:center;gap:14px}.gs-roadmap-number{width:42px;height:42px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:800;flex:0 0 42px}.gs-roadmap-heading{flex:1;min-width:0}.gs-roadmap-tag{font-size:11px;font-weight:800;letter-spacing:.08em}.gs-roadmap-title{font-size:21px;font-weight:800;color:var(--gs-slate);line-height:1.2;margin-top:2px}.gs-roadmap-duration{background:#f6f8f6;border:1px solid #e4ebe5;padding:8px 11px;border-radius:999px;font-size:12px;font-weight:700;color:#52605a;white-space:nowrap}.gs-roadmap-goal{margin:15px 0 12px;color:#46524b;line-height:1.55}.gs-roadmap-checks{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.gs-roadmap-check{display:flex;gap:8px;padding:11px 12px;background:#f9fbf9;border:1px solid #e9efea;border-radius:10px;color:#46524b;font-size:13px;line-height:1.45}.gs-roadmap-check span:first-child{width:22px;height:22px;border-radius:50%;background:#E8F5E9;color:#2E7D32;font-weight:900;display:flex;align-items:center;justify-content:center;flex:0 0 22px}.gs-roadmap-gate{margin-top:13px;padding:10px 12px;border-radius:9px;background:#F1F8E9;color:#33691E;font-size:12px;font-weight:700}.gs-roadmap-connector{width:2px;height:18px;background:#c7d8ca;margin-left:21px}.gs-roadmap-final{display:flex;align-items:flex-start;gap:12px;margin-top:18px}.gs-roadmap-final-icon{width:34px;height:34px;border-radius:10px;background:#E8F5E9;color:#2E7D32;display:flex;align-items:center;justify-content:center;font-weight:900;flex:0 0 34px}@media(max-width:900px){.gs-roadmap-checks{grid-template-columns:1fr}.gs-roadmap-duration{display:none}}

.gs-scheme-hero{display:flex;gap:16px;align-items:center;padding:20px 24px;border-radius:20px;background:linear-gradient(135deg,#E8F5E9 0%,#FFFFFF 72%);border:1px solid var(--gs-border);box-shadow:0 10px 28px rgba(27,94,32,.08);margin-bottom:18px}
.gs-scheme-hero-icon{width:58px;height:58px;border-radius:16px;display:flex;align-items:center;justify-content:center;background:#fff;border:1px solid var(--gs-border);font-size:29px;flex:0 0 58px}.gs-eyebrow{font-size:.72rem;letter-spacing:.12em;font-weight:850;color:var(--gs-green);margin-bottom:3px}.gs-scheme-hero h1{margin:0!important;font-size:2rem!important;color:var(--gs-green-dark)!important}.gs-scheme-hero p{margin:.25rem 0 0!important;color:var(--gs-muted);line-height:1.45}.gs-filter-spacer{height:26px}.gs-scheme-stat{border:1px solid var(--gs-border);border-radius:14px;background:#fff;padding:12px 14px;min-height:88px;display:flex;flex-direction:column;justify-content:center}.gs-scheme-stat span{font-size:17px}.gs-scheme-stat strong{font-size:1.35rem;color:var(--gs-green-dark);line-height:1.1}.gs-scheme-stat small{color:var(--gs-muted);font-size:.75rem;margin-top:4px}.gs-match-note{font-size:.82rem;color:var(--gs-muted);padding:9px 12px;border-radius:10px;background:rgba(232,245,233,.55);margin:6px 0 14px}.gs-scheme-card{border:1px solid var(--gs-border);border-radius:16px;padding:17px 18px;background:#fff;box-shadow:0 6px 20px rgba(27,94,32,.055);margin:8px 0 0}.gs-match-high{border-left:5px solid #2E7D32}.gs-match-mid{border-left:5px solid #EF8B00}.gs-match-low{border-left:5px solid #9E9E9E}.gs-scheme-card-top{display:flex;align-items:center;gap:13px}.gs-scheme-index{width:38px;height:38px;border-radius:11px;background:#F1F8E9;color:#33691E;font-size:.78rem;font-weight:850;display:flex;align-items:center;justify-content:center;flex:0 0 38px}.gs-scheme-card-title{min-width:0;flex:1}.gs-scheme-name{font-size:1.08rem;font-weight:850;color:var(--gs-green-dark);line-height:1.25}.gs-chip-row{display:flex;gap:5px;flex-wrap:wrap;margin-top:6px}.gs-chip{font-size:.68rem;padding:3px 8px;border-radius:999px;background:#F5F7F5;border:1px solid #E3E9E4;color:#5A665E}.gs-match-badge{padding:7px 10px;border-radius:999px;background:#EAF6EC;color:#25612A;font-size:.76rem;font-weight:850;white-space:nowrap}.gs-benefit-strip{display:flex;gap:10px;margin-top:13px;padding:11px 12px;border-radius:11px;background:#F6FBF6;color:#45534A;font-size:.86rem;line-height:1.45}.gs-benefit-strip span{font-size:18px}.gs-detail-panel{border:1px solid #E1E9E2;border-radius:13px;background:#F8FBF8;padding:14px}.gs-detail-label{font-size:.73rem;text-transform:uppercase;letter-spacing:.05em;color:var(--gs-muted);font-weight:800;margin-top:7px}.gs-detail-label:first-child{margin-top:0}.gs-detail-value{font-size:1.08rem;font-weight:850;color:var(--gs-green-dark);margin:4px 0 12px}.gs-progress{height:8px;border-radius:999px;background:#E5EAE6;overflow:hidden;margin-top:6px}.gs-progress div{height:100%;background:#2E7D32;border-radius:999px}.gs-detail-small{font-size:.72rem;color:var(--gs-muted);margin-top:5px}.gs-reason-box{padding:11px 13px;border-radius:11px;background:#F4FAF5;border-left:4px solid #2E7D32;margin:12px 0}.gs-reason-box ul{margin:.35rem 0 0 1.1rem;padding:0}.gs-reason-box li{margin:3px 0;color:#4A554E;font-size:.83rem}
[data-theme="dark"] .gs-scheme-hero,[data-theme="dark"] .gs-scheme-stat,[data-theme="dark"] .gs-scheme-card{background:#141c16}.gs-scheme-hero h1,[data-theme="dark"] .gs-scheme-name{color:#A5D6A7!important}.gs-detail-panel,[data-theme="dark"] .gs-detail-panel{background:#182219;border-color:rgba(144,202,149,.2)}
@media(max-width:800px){.gs-scheme-card-top{align-items:flex-start}.gs-match-badge{font-size:.68rem;padding:6px 8px}.gs-scheme-hero{padding:16px}.gs-scheme-hero-icon{display:none}}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# TRANSLATIONS
# -----------------------------
TEXT = {
    "English": {
        "language": "Language", "location": "Market Location", "navigate": "Navigate",
        "home": "Home", "market": "Market Prices", "schemes": "Government Schemes",
        "finance": "Financial Assistant", "business": "Business Recommendation",
        "welcome": "Welcome to Gram Sahayak",
        "subtitle": "Business & Financial Guidance for Rural Micro-Entrepreneurs",
        "home_desc": "A simple digital assistant designed to help rural micro-entrepreneurs explore local business opportunities, understand sample market conditions, estimate finances and discover relevant government schemes.",
        "crops": "Crops Covered", "locations": "Locations", "schemes_count": "Schemes",
        "business_models": "Business Models", "selected_market": "Selected Market",
        "demo_market": "Current demonstration market", "market_disclaimer": "Market prices shown in this prototype are static sample data for demonstration only.",
        "what_can": "What you can do", "explore": "Explore Markets", "explore_desc": "Compare sample prices across a wider set of crops and locations.",
        "plan": "Plan Finances", "plan_desc": "Estimate profit, revenue, costs and loan EMI before making a decision.",
        "find": "Find a Business", "find_desc": "Get a structured business shortlist based on capital, resources, interests and location.",
        "how": "How Gram Sahayak Works", "how_desc": "Your inputs → local context → rule-based business matching → financial planning → relevant scheme suggestions → practical next steps.",
        "market_title": "Market Prices", "market_desc": "Sample market information for **{location}**. Use it for demonstration and planning only; verify current local mandi prices before making financial decisions.",
        "filter": "Filter by crop category", "all": "All", "board": "Crop Market Board", "showing": "Showing {count} crops for the selected demonstration market: {location}",
        "selected_crop": "Selected Crop", "choose_crop": "Choose a crop", "crop": "Crop", "sample_price": "Sample Price", "trend": "Trend",
        "increasing": "Increasing", "stable": "Stable", "decreasing": "Decreasing",
        "market_note": "Important: location factors and prices are controlled demonstration data for this prototype.",
        "scheme_title": "Government Schemes", "scheme_desc": "Explore schemes that may be relevant to rural entrepreneurs, farmers, vendors, food processors and artisans.",
        "search": "Search schemes", "placeholder": "Example: food, loan, farmer, artisan", "best_for": "Best for",
        "key": "Key information", "why": "Why it may help", "source": "Official source",
        "scheme_warning": "Scheme eligibility, loan approval, subsidy availability and applicable conditions depend on the official guidelines and the applicant's circumstances. Verify details through the relevant Government of India/state portal or bank before applying.",
        "finance_title": "Financial Assistant", "profit_tab": "📊 Profit Calculator", "emi_tab": "🏦 Loan EMI Calculator",
        "profit_est": "Profit Estimator", "quantity": "Quantity", "purchase": "Purchase cost per unit", "selling": "Selling price per unit",
        "other": "Other costs", "total_cost": "Total Cost", "revenue": "Revenue", "profit": "Estimated Profit",
        "positive": "This example produces a positive estimated profit.", "break_even": "This example is approximately at break-even.",
        "loss": "This example produces an estimated loss. Review price and costs.",
        "loan": "Loan amount", "rate": "Annual interest rate (%)", "period": "Loan period (years)", "monthly": "Monthly EMI",
        "total_payment": "Total Payment", "interest": "Total Interest", "loan_note": "Actual loan terms, interest rates, fees and approval depend on the lender.",
        "business_title": "Business Recommendation", "business_desc": "Tell Gram Sahayak about your situation. The prototype will score business models using capital, resources, interest, water availability, experience and location.",
        "capital": "💰 Available capital (₹)", "resource": "🧰 Main available resource", "interest_input": "❤️ Main business interest",
        "water": "💧 Water availability", "experience": "🎯 Your experience", "good": "Good", "limited": "Limited",
        "not_applicable": "Not applicable", "not_sure": "Not sure", "beginner": "Beginner", "some": "Some experience", "experienced": "Experienced",
        "location_note": "📍 Recommendation will be adjusted for the selected market: **{location}**",
        "generate": "🔍 Generate Business Recommendations", "three": "Here are the three strongest prototype matches for your inputs.",
        "match": "Match", "investment": "Indicative investment", "model": "Business model", "why_match": "Why this matches",
        "risk": "Key risk", "steps": "Suggested first steps", "relevant": "Potentially relevant schemes",
        "next_action": "📌 Suggested next action", "below": "Your current capital is below the typical starting range for **{business}**. Consider a smaller pilot, savings, eligible financing or a lower-capital business model.",
        "next": "A practical next step is to prepare a simple cost sheet for **{business}** and compare it with expected local demand before investing.",
        "limit": "Prototype limitation: this is a rule-based recommendation engine using demonstration business profiles. It is a rule-based prototype and does not guarantee profitability.",
        "footer": "🌾 Gram Sahayak • Prototype for rural micro-entrepreneur business guidance",
        "footer_note": "Demo market data • Rule-based recommendations • Verify official scheme information before decisions",
    },
    "Hindi": {
        "language": "भाषा", "location": "बाज़ार स्थान", "navigate": "नेविगेट करें",
        "home": "होम", "market": "बाज़ार भाव", "schemes": "सरकारी योजनाएँ", "finance": "वित्तीय सहायक", "business": "व्यवसाय सुझाव",
        "welcome": "ग्राम सहायक में आपका स्वागत है", "subtitle": "ग्रामीण सूक्ष्म उद्यमियों के लिए व्यवसाय और वित्तीय मार्गदर्शन",
        "home_desc": "ग्रामीण सूक्ष्म उद्यमियों को स्थानीय व्यवसाय के अवसर समझने, नमूना बाज़ार स्थिति देखने, वित्त का अनुमान लगाने और उपयोगी सरकारी योजनाएँ खोजने में मदद करने वाला डिजिटल सहायक।",
        "crops": "शामिल फसलें", "locations": "स्थान", "schemes_count": "योजनाएँ", "business_models": "व्यवसाय मॉडल",
        "selected_market": "चयनित बाज़ार", "demo_market": "वर्तमान प्रदर्शन बाज़ार", "market_disclaimer": "इस प्रोटोटाइप में दिखाए गए बाज़ार भाव नमूना डेटा हैं और लाइव मंडी/API भाव नहीं हैं।",
        "what_can": "आप क्या कर सकते हैं", "explore": "बाज़ार देखें", "explore_desc": "अलग-अलग फसलों और स्थानों के नमूना भावों की तुलना करें।",
        "plan": "वित्त की योजना बनाएं", "plan_desc": "निर्णय लेने से पहले लाभ, राजस्व, लागत और ऋण EMI का अनुमान लगाएं।",
        "find": "व्यवसाय खोजें", "find_desc": "पूंजी, संसाधन, रुचि और स्थान के आधार पर व्यवसायों की सूची पाएं।",
        "how": "ग्राम सहायक कैसे काम करता है", "how_desc": "आपकी जानकारी → स्थानीय संदर्भ → नियम-आधारित व्यवसाय मिलान → वित्तीय योजना → संबंधित योजना सुझाव → अगले व्यावहारिक कदम।",
        "market_title": "बाज़ार भाव", "market_desc": "**{location}** के लिए नमूना बाज़ार जानकारी। इसका उपयोग केवल प्रदर्शन और योजना के लिए करें; वित्तीय निर्णय से पहले वर्तमान स्थानीय मंडी भाव की पुष्टि करें।",
        "filter": "फसल श्रेणी से फ़िल्टर करें", "all": "सभी", "board": "फसल बाज़ार बोर्ड", "showing": "चयनित प्रदर्शन बाज़ार {location} के लिए {count} फसलें दिखाई जा रही हैं",
        "selected_crop": "चयनित फसल", "choose_crop": "फसल चुनें", "crop": "फसल", "sample_price": "नमूना भाव", "trend": "रुझान",
        "increasing": "बढ़ रहा है", "stable": "स्थिर", "decreasing": "घट रहा है", "market_note": "महत्वपूर्ण: स्थान कारक और भाव नियंत्रित प्रदर्शन डेटा हैं, लाइव बाज़ार डेटा नहीं।",
        "scheme_title": "सरकारी योजनाएँ", "scheme_desc": "ग्रामीण उद्यमियों, किसानों, विक्रेताओं, खाद्य प्रसंस्करण इकाइयों और कारीगरों के लिए उपयोगी योजनाएँ देखें।",
        "search": "योजनाएँ खोजें", "placeholder": "उदाहरण: भोजन, ऋण, किसान, कारीगर", "best_for": "किसके लिए", "key": "मुख्य जानकारी", "why": "यह कैसे मदद कर सकती है", "source": "आधिकारिक स्रोत",
        "scheme_warning": "योजना की पात्रता, ऋण स्वीकृति, सब्सिडी और शर्तें आधिकारिक दिशानिर्देश तथा आवेदक की स्थिति पर निर्भर करती हैं। आवेदन से पहले संबंधित सरकारी पोर्टल या बैंक से जानकारी सत्यापित करें।",
        "finance_title": "वित्तीय सहायक", "profit_tab": "📊 लाभ कैलकुलेटर", "emi_tab": "🏦 ऋण EMI कैलकुलेटर",
        "profit_est": "लाभ अनुमान", "quantity": "मात्रा", "purchase": "प्रति इकाई खरीद लागत", "selling": "प्रति इकाई बिक्री मूल्य", "other": "अन्य लागत",
        "total_cost": "कुल लागत", "revenue": "राजस्व", "profit": "अनुमानित लाभ", "positive": "इस उदाहरण में अनुमानित लाभ सकारात्मक है।",
        "break_even": "यह उदाहरण लगभग ब्रेक-ईवन पर है।", "loss": "इस उदाहरण में अनुमानित नुकसान है। मूल्य और लागत की समीक्षा करें।",
        "loan": "ऋण राशि", "rate": "वार्षिक ब्याज दर (%)", "period": "ऋण अवधि (वर्ष)", "monthly": "मासिक EMI", "total_payment": "कुल भुगतान", "interest": "कुल ब्याज",
        "loan_note": "वास्तविक ऋण शर्तें, ब्याज दर, शुल्क और स्वीकृति ऋणदाता पर निर्भर करते हैं।",
        "business_title": "व्यवसाय सुझाव", "business_desc": "अपनी स्थिति के बारे में ग्राम सहायक को बताएं। प्रोटोटाइप पूंजी, संसाधन, रुचि, पानी, अनुभव और स्थान के आधार पर व्यवसायों का स्कोर करेगा।",
        "capital": "💰 उपलब्ध पूंजी (₹)", "resource": "🧰 मुख्य उपलब्ध संसाधन", "interest_input": "❤️ मुख्य व्यवसाय रुचि", "water": "💧 पानी की उपलब्धता",
        "experience": "🎯 आपका अनुभव", "good": "अच्छी", "limited": "सीमित", "not_applicable": "लागू नहीं", "not_sure": "पता नहीं",
        "beginner": "शुरुआती", "some": "कुछ अनुभव", "experienced": "अनुभवी", "location_note": "📍 चुने गए बाज़ार के अनुसार सुझाव बदला जाएगा: **{location}**",
        "generate": "🔍 व्यवसाय सुझाव बनाएं", "three": "आपकी जानकारी के आधार पर तीन सबसे मजबूत प्रोटोटाइप सुझाव ये हैं।", "match": "मिलान",
        "investment": "अनुमानित निवेश", "model": "व्यवसाय मॉडल", "why_match": "यह क्यों उपयुक्त है", "risk": "मुख्य जोखिम", "steps": "सुझाए गए शुरुआती कदम", "relevant": "संभावित संबंधित योजनाएँ",
        "next_action": "📌 सुझाया गया अगला कदम", "below": "आपकी वर्तमान पूंजी **{business}** के सामान्य शुरुआती निवेश से कम है। छोटे पायलट, बचत, पात्र वित्तपोषण या कम पूंजी वाले व्यवसाय पर विचार करें।",
        "next": "अगला व्यावहारिक कदम **{business}** की सरल लागत सूची बनाना और निवेश से पहले अपेक्षित स्थानीय मांग से उसकी तुलना करना है।",
        "limit": "प्रोटोटाइप सीमा: यह प्रदर्शन व्यवसाय प्रोफाइल पर आधारित नियम-आधारित सिफारिश इंजन है। यह लाइव AI मॉडल नहीं है और लाभ की गारंटी नहीं देता।",
        "footer": "🌾 ग्राम सहायक • ग्रामीण सूक्ष्म उद्यम व्यवसाय मार्गदर्शन प्रोटोटाइप", "footer_note": "डेमो बाज़ार डेटा • नियम-आधारित सुझाव • निर्णय से पहले आधिकारिक योजना जानकारी सत्यापित करें",
    },
    "Kannada": {
        "language": "ಭಾಷೆ", "location": "ಮಾರುಕಟ್ಟೆ ಸ್ಥಳ", "navigate": "ನ್ಯಾವಿಗೇಟ್ ಮಾಡಿ",
        "home": "ಮುಖಪುಟ", "market": "ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳು", "schemes": "ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು", "finance": "ಹಣಕಾಸು ಸಹಾಯಕ", "business": "ವ್ಯವಹಾರ ಶಿಫಾರಸು",
        "welcome": "ಗ್ರಾಮ ಸಹಾಯಕಕ್ಕೆ ಸ್ವಾಗತ", "subtitle": "ಗ್ರಾಮೀಣ ಸಣ್ಣ ಉದ್ಯಮಿಗಳಿಗೆ ವ್ಯವಹಾರ ಮತ್ತು ಹಣಕಾಸು ಮಾರ್ಗದರ್ಶನ",
        "home_desc": "ಗ್ರಾಮೀಣ ಸಣ್ಣ ಉದ್ಯಮಿಗಳಿಗೆ ಸ್ಥಳೀಯ ವ್ಯವಹಾರ ಅವಕಾಶಗಳನ್ನು ತಿಳಿದುಕೊಳ್ಳಲು, ಮಾದರಿ ಮಾರುಕಟ್ಟೆ ಪರಿಸ್ಥಿತಿಯನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳಲು, ಹಣಕಾಸು ಅಂದಾಜು ಮಾಡಲು ಮತ್ತು ಸಂಬಂಧಿತ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳನ್ನು ಹುಡುಕಲು ಸಹಾಯ ಮಾಡುವ ಡಿಜಿಟಲ್ ಸಹಾಯಕ.",
        "crops": "ಒಳಗೊಂಡ ಬೆಳೆಗಳು", "locations": "ಸ್ಥಳಗಳು", "schemes_count": "ಯೋಜನೆಗಳು", "business_models": "ವ್ಯವಹಾರ ಮಾದರಿಗಳು",
        "selected_market": "ಆಯ್ಕೆ ಮಾಡಿದ ಮಾರುಕಟ್ಟೆ", "demo_market": "ಪ್ರಸ್ತುತ ಪ್ರದರ್ಶನ ಮಾರುಕಟ್ಟೆ", "market_disclaimer": "ಈ ಪ್ರೋಟೋಟೈಪ್‌ನಲ್ಲಿರುವ ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳು ಮಾದರಿ ಡೇಟಾ ಮಾತ್ರ; ಇವು ಲೈವ್ ಮಂಡಿ/API ಬೆಲೆಗಳಲ್ಲ.",
        "what_can": "ನೀವು ಏನು ಮಾಡಬಹುದು", "explore": "ಮಾರುಕಟ್ಟೆಗಳನ್ನು ನೋಡಿ", "explore_desc": "ವಿವಿಧ ಬೆಳೆಗಳು ಮತ್ತು ಸ್ಥಳಗಳ ಮಾದರಿ ಬೆಲೆಗಳನ್ನು ಹೋಲಿಸಿ.",
        "plan": "ಹಣಕಾಸು ಯೋಜಿಸಿ", "plan_desc": "ನಿರ್ಧಾರಕ್ಕೂ ಮೊದಲು ಲಾಭ, ಆದಾಯ, ವೆಚ್ಚ ಮತ್ತು ಸಾಲದ EMI ಅಂದಾಜಿಸಿ.",
        "find": "ವ್ಯವಹಾರ ಹುಡುಕಿ", "find_desc": "ಬಂಡವಾಳ, ಸಂಪನ್ಮೂಲ, ಆಸಕ್ತಿ ಮತ್ತು ಸ್ಥಳದ ಆಧಾರದ ಮೇಲೆ ವ್ಯವಹಾರಗಳ ಪಟ್ಟಿಯನ್ನು ಪಡೆಯಿರಿ.",
        "how": "ಗ್ರಾಮ ಸಹಾಯಕ ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ", "how_desc": "ನಿಮ್ಮ ಮಾಹಿತಿ → ಸ್ಥಳೀಯ ಸಂದರ್ಭ → ನಿಯಮಾಧಾರಿತ ವ್ಯವಹಾರ ಹೊಂದಾಣಿಕೆ → ಹಣಕಾಸು ಯೋಜನೆ → ಸಂಬಂಧಿತ ಯೋಜನೆ ಸಲಹೆಗಳು → ಮುಂದಿನ ಪ್ರಾಯೋಗಿಕ ಹಂತಗಳು.",
        "market_title": "ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳು", "market_desc": "**{location}** ಗಾಗಿ ಮಾದರಿ ಮಾರುಕಟ್ಟೆ ಮಾಹಿತಿ. ಇದನ್ನು ಪ್ರದರ್ಶನ ಮತ್ತು ಯೋಜನೆಗಾಗಿ ಮಾತ್ರ ಬಳಸಿ; ಹಣಕಾಸು ನಿರ್ಧಾರಕ್ಕೂ ಮೊದಲು ಪ್ರಸ್ತುತ ಸ್ಥಳೀಯ ಮಂಡಿ ಬೆಲೆಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.",
        "filter": "ಬೆಳೆ ವರ್ಗದ ಮೂಲಕ ಫಿಲ್ಟರ್ ಮಾಡಿ", "all": "ಎಲ್ಲಾ", "board": "ಬೆಳೆ ಮಾರುಕಟ್ಟೆ ಫಲಕ", "showing": "ಆಯ್ಕೆ ಮಾಡಿದ ಪ್ರದರ್ಶನ ಮಾರುಕಟ್ಟೆ {location} ಗಾಗಿ {count} ಬೆಳೆಗಳನ್ನು ತೋರಿಸಲಾಗುತ್ತಿದೆ",
        "selected_crop": "ಆಯ್ಕೆ ಮಾಡಿದ ಬೆಳೆ", "choose_crop": "ಬೆಳೆ ಆಯ್ಕೆ ಮಾಡಿ", "crop": "ಬೆಳೆ", "sample_price": "ಮಾದರಿ ಬೆಲೆ", "trend": "ಪ್ರವೃತ್ತಿ",
        "increasing": "ಏರಿಕೆ", "stable": "ಸ್ಥಿರ", "decreasing": "ಇಳಿಕೆ", "market_note": "ಮುಖ್ಯ: ಸ್ಥಳದ ಅಂಶಗಳು ಮತ್ತು ಬೆಲೆಗಳು ನಿಯಂತ್ರಿತ ಪ್ರದರ್ಶನ ಡೇಟಾ; ಲೈವ್ ಮಾರುಕಟ್ಟೆ ಫೀಡ್ ಅಲ್ಲ.",
        "scheme_title": "ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು", "scheme_desc": "ಗ್ರಾಮೀಣ ಉದ್ಯಮಿಗಳು, ರೈತರು, ಮಾರಾಟಗಾರರು, ಆಹಾರ ಸಂಸ್ಕರಣಾ ಘಟಕಗಳು ಮತ್ತು ಕರಕುಶಲಗಾರರಿಗೆ ಸಂಬಂಧಿಸಿದ ಯೋಜನೆಗಳನ್ನು ನೋಡಿ.",
        "search": "ಯೋಜನೆಗಳನ್ನು ಹುಡುಕಿ", "placeholder": "ಉದಾಹರಣೆ: ಆಹಾರ, ಸಾಲ, ರೈತ, ಕರಕುಶಲಗಾರ", "best_for": "ಯಾರಿಗೆ ಸೂಕ್ತ", "key": "ಮುಖ್ಯ ಮಾಹಿತಿ", "why": "ಇದು ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು", "source": "ಅಧಿಕೃತ ಮೂಲ",
        "scheme_warning": "ಯೋಜನೆಯ ಅರ್ಹತೆ, ಸಾಲ ಅನುಮೋದನೆ, ಸಬ್ಸಿಡಿ ಮತ್ತು ಷರತ್ತುಗಳು ಅಧಿಕೃತ ಮಾರ್ಗಸೂಚಿಗಳು ಮತ್ತು ಅರ್ಜಿದಾರರ ಪರಿಸ್ಥಿತಿಯ ಮೇಲೆ ಅವಲಂಬಿತವಾಗಿವೆ. ಅರ್ಜಿ ಸಲ್ಲಿಸುವ ಮೊದಲು ಸಂಬಂಧಿತ ಸರ್ಕಾರಿ ಪೋರ್ಟಲ್ ಅಥವಾ ಬ್ಯಾಂಕ್ ಮೂಲಕ ವಿವರಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.",
        "finance_title": "ಹಣಕಾಸು ಸಹಾಯಕ", "profit_tab": "📊 ಲಾಭ ಕ್ಯಾಲ್ಕುಲೇಟರ್", "emi_tab": "🏦 ಸಾಲ EMI ಕ್ಯಾಲ್ಕುಲೇಟರ್",
        "profit_est": "ಲಾಭ ಅಂದಾಜು", "quantity": "ಪ್ರಮಾಣ", "purchase": "ಪ್ರತಿ ಘಟಕ ಖರೀದಿ ವೆಚ್ಚ", "selling": "ಪ್ರತಿ ಘಟಕ ಮಾರಾಟ ಬೆಲೆ", "other": "ಇತರೆ ವೆಚ್ಚಗಳು",
        "total_cost": "ಒಟ್ಟು ವೆಚ್ಚ", "revenue": "ಆದಾಯ", "profit": "ಅಂದಾಜು ಲಾಭ", "positive": "ಈ ಉದಾಹರಣೆಯಲ್ಲಿ ಅಂದಾಜು ಲಾಭ ಧನಾತ್ಮಕವಾಗಿದೆ.",
        "break_even": "ಈ ಉದಾಹರಣೆ ಸುಮಾರು ಬ್ರೇಕ್-ಈವನ್ ಸ್ಥಿತಿಯಲ್ಲಿದೆ.", "loss": "ಈ ಉದಾಹರಣೆಯಲ್ಲಿ ಅಂದಾಜು ನಷ್ಟವಿದೆ. ಬೆಲೆ ಮತ್ತು ವೆಚ್ಚಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.",
        "loan": "ಸಾಲದ ಮೊತ್ತ", "rate": "ವಾರ್ಷಿಕ ಬಡ್ಡಿ ದರ (%)", "period": "ಸಾಲದ ಅವಧಿ (ವರ್ಷಗಳು)", "monthly": "ಮಾಸಿಕ EMI", "total_payment": "ಒಟ್ಟು ಪಾವತಿ", "interest": "ಒಟ್ಟು ಬಡ್ಡಿ",
        "loan_note": "ನಿಜವಾದ ಸಾಲದ ಷರತ್ತುಗಳು, ಬಡ್ಡಿದರ, ಶುಲ್ಕಗಳು ಮತ್ತು ಅನುಮೋದನೆ ಸಾಲದಾತರ ಮೇಲೆ ಅವಲಂಬಿತವಾಗಿವೆ.",
        "business_title": "ವ್ಯವಹಾರ ಶಿಫಾರಸು", "business_desc": "ನಿಮ್ಮ ಪರಿಸ್ಥಿತಿಯನ್ನು ಗ್ರಾಮ ಸಹಾಯಕಕ್ಕೆ ತಿಳಿಸಿ. ಪ್ರೋಟೋಟೈಪ್ ಬಂಡವಾಳ, ಸಂಪನ್ಮೂಲ, ಆಸಕ್ತಿ, ನೀರಿನ ಲಭ್ಯತೆ, ಅನುಭವ ಮತ್ತು ಸ್ಥಳದ ಆಧಾರದ ಮೇಲೆ ವ್ಯವಹಾರಗಳಿಗೆ ಅಂಕ ನೀಡುತ್ತದೆ.",
        "capital": "💰 ಲಭ್ಯವಿರುವ ಬಂಡವಾಳ (₹)", "resource": "🧰 ಮುಖ್ಯ ಲಭ್ಯವಿರುವ ಸಂಪನ್ಮೂಲ", "interest_input": "❤️ ಮುಖ್ಯ ವ್ಯವಹಾರ ಆಸಕ್ತಿ", "water": "💧 ನೀರಿನ ಲಭ್ಯತೆ",
        "experience": "🎯 ನಿಮ್ಮ ಅನುಭವ", "good": "ಉತ್ತಮ", "limited": "ಸೀಮಿತ", "not_applicable": "ಅನ್ವಯಿಸುವುದಿಲ್ಲ", "not_sure": "ಖಚಿತವಿಲ್ಲ",
        "beginner": "ಆರಂಭಿಕ", "some": "ಸ್ವಲ್ಪ ಅನುಭವ", "experienced": "ಅನುಭವ ಹೊಂದಿರುವವರು", "location_note": "📍 ಆಯ್ಕೆ ಮಾಡಿದ ಮಾರುಕಟ್ಟೆಗೆ ಅನುಗುಣವಾಗಿ ಶಿಫಾರಸು ಬದಲಾಗುತ್ತದೆ: **{location}**",
        "generate": "🔍 ವ್ಯವಹಾರ ಶಿಫಾರಸುಗಳನ್ನು ರಚಿಸಿ", "three": "ನಿಮ್ಮ ಮಾಹಿತಿಗೆ ಹೊಂದುವ ಮೂರು ಉತ್ತಮ ಪ್ರೋಟೋಟೈಪ್ ಶಿಫಾರಸುಗಳು ಇಲ್ಲಿವೆ.", "match": "ಹೊಂದಾಣಿಕೆ",
        "investment": "ಅಂದಾಜು ಹೂಡಿಕೆ", "model": "ವ್ಯವಹಾರ ಮಾದರಿ", "why_match": "ಇದು ಏಕೆ ಹೊಂದಿಕೊಳ್ಳುತ್ತದೆ", "risk": "ಮುಖ್ಯ ಅಪಾಯ", "steps": "ಸೂಚಿಸಿದ ಆರಂಭಿಕ ಹಂತಗಳು", "relevant": "ಸಂಬಂಧಿತವಾಗಿರಬಹುದಾದ ಯೋಜನೆಗಳು",
        "next_action": "📌 ಸೂಚಿಸಿದ ಮುಂದಿನ ಕ್ರಮ", "below": "ನಿಮ್ಮ ಪ್ರಸ್ತುತ ಬಂಡವಾಳವು **{business}** ಗೆ ಸಾಮಾನ್ಯ ಆರಂಭಿಕ ಹೂಡಿಕೆಗಿಂತ ಕಡಿಮೆಯಾಗಿದೆ. ಸಣ್ಣ ಪೈಲಟ್, ಉಳಿತಾಯ, ಅರ್ಹ ಹಣಕಾಸು ಅಥವಾ ಕಡಿಮೆ ಬಂಡವಾಳದ ವ್ಯವಹಾರವನ್ನು ಪರಿಗಣಿಸಿ.",
        "next": "ಮುಂದಿನ ಪ್ರಾಯೋಗಿಕ ಹಂತವೆಂದರೆ **{business}** ಗಾಗಿ ಸರಳ ವೆಚ್ಚಪಟ್ಟಿ ತಯಾರಿಸಿ, ಹೂಡಿಕೆ ಮಾಡುವ ಮೊದಲು ನಿರೀಕ್ಷಿತ ಸ್ಥಳೀಯ ಬೇಡಿಕೆಯೊಂದಿಗೆ ಹೋಲಿಸುವುದು.",
        "limit": "ಪ್ರೋಟೋಟೈಪ್ ಮಿತಿ: ಇದು ಪ್ರದರ್ಶನ ವ್ಯವಹಾರ ಪ್ರೊಫೈಲ್‌ಗಳನ್ನು ಬಳಸುವ ನಿಯಮಾಧಾರಿತ ಶಿಫಾರಸು ಎಂಜಿನ್. ಇದು ಲೈವ್ AI ಮಾದರಿ ಅಲ್ಲ ಮತ್ತು ಲಾಭದ ಖಾತರಿ ನೀಡುವುದಿಲ್ಲ.",
        "footer": "🌾 ಗ್ರಾಮ ಸಹಾಯಕ • ಗ್ರಾಮೀಣ ಸಣ್ಣ ಉದ್ಯಮ ವ್ಯವಹಾರ ಮಾರ್ಗದರ್ಶನ ಪ್ರೋಟೋಟೈಪ್", "footer_note": "ಡೆಮೊ ಮಾರುಕಟ್ಟೆ ಡೇಟಾ • ನಿಯಮಾಧಾರಿತ ಶಿಫಾರಸುಗಳು • ನಿರ್ಧಾರಕ್ಕೂ ಮೊದಲು ಅಧಿಕೃತ ಯೋಜನೆ ಮಾಹಿತಿಯನ್ನು ಪರಿಶೀಲಿಸಿ",
    }
}

# -----------------------------
# EXTRA TRANSLATIONS (new features)
# Merged into TEXT so tr() keeps working the same way everywhere.
# Anything not translated for Hindi/Kannada gracefully falls back to English
# via the existing tr() lookup — same pattern already used across this file.
# -----------------------------
EXTRA_TEXT = {
    "English": {
        "crop_location_filter": "🌍 Show only crops suited to this location",
        "crop_location_note": "Suitability is based on this prototype's demonstration agro-climatic profile for each location.",
        "no_crops_for_location": "No demonstration crops are marked suitable for this location yet — showing all crops instead.",
        "resource_section_title": "🧾 Detailed resource availability (add one or more)",
        "resource_section_desc": "Add each land/resource you have access to, with its specifications. This improves the accuracy of the match, timeline and risk analysis.",
        "add_resource": "➕ Add another resource",
        "remove_resource": "🗑️ Remove this resource",
        "resource_n": "Resource",
        "resource_type_label": "Resource type",
        "land_area_label": "Area of land (acres)",
        "water_qty_label": "Amount of water available",
        "climate_label": "Climate in this land",
        "labor_label": "Labour available (people)",
        "market_access_label": "Market access",
        "water_none": "None / rain-fed only",
        "water_low": "Low (borewell/limited)",
        "water_medium": "Medium (seasonal canal/tank)",
        "water_high": "High (canal/river/reliable borewell)",
        "climate_dry": "Dry / semi-arid",
        "climate_moderate": "Moderate",
        "climate_humid": "Humid / high rainfall",
        "climate_hilly": "Hilly / cooler",
        "market_poor": "Poor (far from mandi/town)",
        "market_moderate": "Moderate (nearby town)",
        "market_good": "Good (close to mandi/city, transport available)",
        "no_resources_added": "No detailed resources added yet. You can still generate recommendations using the basic inputs above.",
        "success_rate_label": "📊 Estimated feasibility indicator",
        "timeline_label": "⏱️ Typical timeline to profitability",
        "return_label": "📈 Indicative annual return on investment",
        "months": "months",
        "view_details_btn": "🔍 View in-depth analysis",
        "back_to_results": "← Back to all recommendations",
        "deep_dive_title": "In-depth analysis",
        "deep_dive_crops_title": "🌱 Crops that can be grown at this location",
        "deep_dive_crops_none": "This business is not primarily crop-based, so no crop list is shown here.",
        "deep_dive_scheme_title": "🏛️ How each suggested scheme can help",
        "deep_dive_risk_title": "⚠️ Detailed risk analysis",
        "risk_category": "Category", "risk_likelihood": "Likelihood", "risk_impact": "Impact", "risk_mitigation": "Suggested mitigation",
        "deep_dive_invest_title": "💰 Investment vs. expected benefit calculator",
        "min_investment": "Minimum recommended investment for this business",
        "your_investment_input": "Enter an investment amount to check",
        "estimated_annual_benefit": "Indicative estimated annual benefit",
        "estimated_timeline_result": "Indicative timeline before this becomes visible",
        "investment_below_min_warning": "This amount is below the minimum indicative range for this business. Returns and timelines become less predictable below this level.",
        "investment_disclaimer": "These are prototype estimates based on demonstration success-rate and return assumptions for similar rural micro-enterprises. They are not a guarantee of profit and do not replace a proper business plan.",
        "compare_table_title": "Benefit at a few investment levels",
        "invest_level": "Investment", "invest_benefit": "Indicative annual benefit range",
    },
    "Hindi": {
        "crop_location_filter": "🌍 केवल इस स्थान के लिए उपयुक्त फसलें दिखाएँ",
        "crop_location_note": "उपयुक्तता इस प्रोटोटाइप के प्रत्येक स्थान के प्रदर्शन कृषि-जलवायु प्रोफाइल पर आधारित है।",
        "no_crops_for_location": "इस स्थान के लिए अभी कोई नमूना फसल चिह्नित नहीं है — इसलिए सभी फसलें दिखाई जा रही हैं।",
        "resource_section_title": "🧾 विस्तृत संसाधन उपलब्धता (एक या अधिक जोड़ें)",
        "resource_section_desc": "आपके पास मौजूद प्रत्येक भूमि/संसाधन को उसकी विशेषताओं के साथ जोड़ें। इससे मिलान, समयसीमा और जोखिम विश्लेषण अधिक सटीक होगा।",
        "add_resource": "➕ एक और संसाधन जोड़ें",
        "remove_resource": "🗑️ यह संसाधन हटाएँ",
        "resource_n": "संसाधन",
        "resource_type_label": "संसाधन प्रकार",
        "land_area_label": "भूमि का क्षेत्रफल (एकड़)",
        "water_qty_label": "उपलब्ध पानी की मात्रा",
        "climate_label": "इस भूमि की जलवायु",
        "labor_label": "उपलब्ध श्रमिक (संख्या)",
        "market_access_label": "बाज़ार तक पहुँच",
        "water_none": "नहीं / केवल वर्षा आधारित",
        "water_low": "कम (बोरवेल/सीमित)",
        "water_medium": "मध्यम (मौसमी नहर/तालाब)",
        "water_high": "अधिक (नहर/नदी/भरोसेमंद बोरवेल)",
        "climate_dry": "शुष्क / अर्ध-शुष्क",
        "climate_moderate": "सामान्य",
        "climate_humid": "आर्द्र / अधिक वर्षा",
        "climate_hilly": "पहाड़ी / ठंडा",
        "market_poor": "कमज़ोर (मंडी/शहर से दूर)",
        "market_moderate": "मध्यम (नजदीकी कस्बा)",
        "market_good": "अच्छा (मंडी/शहर के पास, परिवहन उपलब्ध)",
        "no_resources_added": "अभी तक कोई विस्तृत संसाधन नहीं जोड़ा गया। आप ऊपर दी गई बुनियादी जानकारी से भी सुझाव प्राप्त कर सकते हैं।",
        "success_rate_label": "📊 अनुमानित सफलता दर",
        "timeline_label": "⏱️ लाभदायक होने की सामान्य समयसीमा",
        "return_label": "📈 अनुमानित वार्षिक निवेश प्रतिफल",
        "months": "महीने",
        "view_details_btn": "🔍 विस्तृत विश्लेषण देखें",
        "back_to_results": "← सभी सुझावों पर वापस जाएँ",
        "deep_dive_title": "विस्तृत विश्लेषण",
        "deep_dive_crops_title": "🌱 इस स्थान पर उगाई जा सकने वाली फसलें",
        "deep_dive_crops_none": "यह व्यवसाय मुख्यतः फसल-आधारित नहीं है, इसलिए यहाँ फसल सूची नहीं दिखाई गई है।",
        "deep_dive_scheme_title": "🏛️ हर सुझाई गई योजना कैसे मदद कर सकती है",
        "deep_dive_risk_title": "⚠️ विस्तृत जोखिम विश्लेषण",
        "risk_category": "श्रेणी", "risk_likelihood": "संभावना", "risk_impact": "प्रभाव", "risk_mitigation": "सुझाया गया समाधान",
        "deep_dive_invest_title": "💰 निवेश बनाम अनुमानित लाभ कैलकुलेटर",
        "min_investment": "इस व्यवसाय के लिए न्यूनतम अनुशंसित निवेश",
        "your_investment_input": "जाँचने के लिए निवेश राशि दर्ज करें",
        "estimated_annual_benefit": "अनुमानित वार्षिक लाभ",
        "estimated_timeline_result": "यह प्रभाव दिखने की अनुमानित समयसीमा",
        "investment_below_min_warning": "यह राशि इस व्यवसाय की न्यूनतम अनुशंसित सीमा से कम है। इस स्तर से नीचे प्रतिफल और समयसीमा कम अनुमानित होती है।",
        "investment_disclaimer": "ये अनुमान समान ग्रामीण सूक्ष्म उद्यमों के लिए प्रदर्शन सफलता-दर और प्रतिफल मान्यताओं पर आधारित प्रोटोटाइप अनुमान हैं। यह लाभ की गारंटी नहीं है और उचित व्यवसाय योजना का विकल्प नहीं है।",
        "compare_table_title": "कुछ निवेश स्तरों पर लाभ",
        "invest_level": "निवेश", "invest_benefit": "अनुमानित वार्षिक लाभ सीमा",
    },
    "Kannada": {
        "crop_location_filter": "🌍 ಈ ಸ್ಥಳಕ್ಕೆ ಸೂಕ್ತವಾದ ಬೆಳೆಗಳನ್ನು ಮಾತ್ರ ತೋರಿಸಿ",
        "crop_location_note": "ಸೂಕ್ತತೆಯು ಈ ಪ್ರೋಟೋಟೈಪ್‌ನ ಪ್ರತಿ ಸ್ಥಳದ ಪ್ರದರ್ಶನ ಕೃಷಿ-ಹವಾಮಾನ ಪ್ರೊಫೈಲ್ ಆಧಾರಿತವಾಗಿದೆ.",
        "no_crops_for_location": "ಈ ಸ್ಥಳಕ್ಕೆ ಇನ್ನೂ ಯಾವುದೇ ಮಾದರಿ ಬೆಳೆ ಗುರುತಿಸಲಾಗಿಲ್ಲ — ಬದಲಿಗೆ ಎಲ್ಲಾ ಬೆಳೆಗಳನ್ನು ತೋರಿಸಲಾಗುತ್ತಿದೆ.",
        "resource_section_title": "🧾 ವಿವರವಾದ ಸಂಪನ್ಮೂಲ ಲಭ್ಯತೆ (ಒಂದು ಅಥವಾ ಹೆಚ್ಚು ಸೇರಿಸಿ)",
        "resource_section_desc": "ನಿಮ್ಮ ಬಳಿ ಇರುವ ಪ್ರತಿ ಭೂಮಿ/ಸಂಪನ್ಮೂಲವನ್ನು ಅದರ ವಿವರಗಳೊಂದಿಗೆ ಸೇರಿಸಿ. ಇದು ಹೊಂದಾಣಿಕೆ, ಸಮಯಪಟ್ಟಿ ಮತ್ತು ಅಪಾಯ ವಿಶ್ಲೇಷಣೆಯ ನಿಖರತೆಯನ್ನು ಸುಧಾರಿಸುತ್ತದೆ.",
        "add_resource": "➕ ಇನ್ನೊಂದು ಸಂಪನ್ಮೂಲ ಸೇರಿಸಿ",
        "remove_resource": "🗑️ ಈ ಸಂಪನ್ಮೂಲ ತೆಗೆದುಹಾಕಿ",
        "resource_n": "ಸಂಪನ್ಮೂಲ",
        "resource_type_label": "ಸಂಪನ್ಮೂಲ ಪ್ರಕಾರ",
        "land_area_label": "ಭೂಮಿಯ ವಿಸ್ತೀರ್ಣ (ಎಕರೆ)",
        "water_qty_label": "ಲಭ್ಯವಿರುವ ನೀರಿನ ಪ್ರಮಾಣ",
        "climate_label": "ಈ ಭೂಮಿಯ ಹವಾಮಾನ",
        "labor_label": "ಲಭ್ಯವಿರುವ ಕಾರ್ಮಿಕರು (ಸಂಖ್ಯೆ)",
        "market_access_label": "ಮಾರುಕಟ್ಟೆ ಪ್ರವೇಶ",
        "water_none": "ಇಲ್ಲ / ಕೇವಲ ಮಳೆ ಆಧಾರಿತ",
        "water_low": "ಕಡಿಮೆ (ಬೋರ್‌ವೆಲ್/ಸೀಮಿತ)",
        "water_medium": "ಮಧ್ಯಮ (ಋತುಮಾನ ಕಾಲುವೆ/ಕೆರೆ)",
        "water_high": "ಹೆಚ್ಚು (ಕಾಲುವೆ/ನದಿ/ವಿಶ್ವಾಸಾರ್ಹ ಬೋರ್‌ವೆಲ್)",
        "climate_dry": "ಒಣ / ಅರೆ-ಶುಷ್ಕ",
        "climate_moderate": "ಸಾಧಾರಣ",
        "climate_humid": "ಆರ್ದ್ರ / ಹೆಚ್ಚು ಮಳೆ",
        "climate_hilly": "ಗುಡ್ಡಗಾಡು / ತಂಪಾದ",
        "market_poor": "ಕಡಿಮೆ (ಮಂಡಿ/ಪಟ್ಟಣದಿಂದ ದೂರ)",
        "market_moderate": "ಮಧ್ಯಮ (ಹತ್ತಿರದ ಪಟ್ಟಣ)",
        "market_good": "ಉತ್ತಮ (ಮಂಡಿ/ನಗರದ ಹತ್ತಿರ, ಸಾರಿಗೆ ಲಭ್ಯ)",
        "no_resources_added": "ಇನ್ನೂ ಯಾವುದೇ ವಿವರವಾದ ಸಂಪನ್ಮೂಲ ಸೇರಿಸಿಲ್ಲ. ಮೇಲಿನ ಮೂಲ ಮಾಹಿತಿಯಿಂದಲೂ ನೀವು ಶಿಫಾರಸುಗಳನ್ನು ಪಡೆಯಬಹುದು.",
        "success_rate_label": "📊 ಅಂದಾಜು ಯಶಸ್ಸಿನ ದರ",
        "timeline_label": "⏱️ ಲಾಭದಾಯಕವಾಗಲು ಸಾಮಾನ್ಯ ಸಮಯಪಟ್ಟಿ",
        "return_label": "📈 ಅಂದಾಜು ವಾರ್ಷಿಕ ಹೂಡಿಕೆ ಪ್ರತಿಫಲ",
        "months": "ತಿಂಗಳುಗಳು",
        "view_details_btn": "🔍 ವಿವರವಾದ ವಿಶ್ಲೇಷಣೆ ನೋಡಿ",
        "back_to_results": "← ಎಲ್ಲಾ ಶಿಫಾರಸುಗಳಿಗೆ ಹಿಂತಿರುಗಿ",
        "deep_dive_title": "ವಿವರವಾದ ವಿಶ್ಲೇಷಣೆ",
        "deep_dive_crops_title": "🌱 ಈ ಸ್ಥಳದಲ್ಲಿ ಬೆಳೆಯಬಹುದಾದ ಬೆಳೆಗಳು",
        "deep_dive_crops_none": "ಈ ವ್ಯವಹಾರವು ಮುಖ್ಯವಾಗಿ ಬೆಳೆ-ಆಧಾರಿತವಲ್ಲ, ಆದ್ದರಿಂದ ಇಲ್ಲಿ ಬೆಳೆ ಪಟ್ಟಿ ತೋರಿಸಲಾಗಿಲ್ಲ.",
        "deep_dive_scheme_title": "🏛️ ಪ್ರತಿ ಶಿಫಾರಸು ಮಾಡಿದ ಯೋಜನೆ ಹೇಗೆ ಸಹಾಯ ಮಾಡಬಹುದು",
        "deep_dive_risk_title": "⚠️ ವಿವರವಾದ ಅಪಾಯ ವಿಶ್ಲೇಷಣೆ",
        "risk_category": "ವರ್ಗ", "risk_likelihood": "ಸಾಧ್ಯತೆ", "risk_impact": "ಪರಿಣಾಮ", "risk_mitigation": "ಸೂಚಿಸಿದ ಪರಿಹಾರ",
        "deep_dive_invest_title": "💰 ಹೂಡಿಕೆ ಮತ್ತು ಅಂದಾಜು ಲಾಭ ಕ್ಯಾಲ್ಕುಲೇಟರ್",
        "min_investment": "ಈ ವ್ಯವಹಾರಕ್ಕೆ ಕನಿಷ್ಠ ಶಿಫಾರಸು ಮಾಡಿದ ಹೂಡಿಕೆ",
        "your_investment_input": "ಪರಿಶೀಲಿಸಲು ಹೂಡಿಕೆ ಮೊತ್ತ ನಮೂದಿಸಿ",
        "estimated_annual_benefit": "ಅಂದಾಜು ವಾರ್ಷಿಕ ಲಾಭ",
        "estimated_timeline_result": "ಇದು ಗೋಚರಿಸುವ ಅಂದಾಜು ಸಮಯಪಟ್ಟಿ",
        "investment_below_min_warning": "ಈ ಮೊತ್ತವು ಈ ವ್ಯವಹಾರದ ಕನಿಷ್ಠ ಶಿಫಾರಸು ವ್ಯಾಪ್ತಿಗಿಂತ ಕಡಿಮೆಯಿದೆ. ಈ ಮಟ್ಟಕ್ಕಿಂತ ಕಡಿಮೆ ಪ್ರತಿಫಲ ಮತ್ತು ಸಮಯಪಟ್ಟಿ ಕಡಿಮೆ ಊಹಿಸಬಹುದಾಗಿರುತ್ತದೆ.",
        "investment_disclaimer": "ಇವು ಇದೇ ರೀತಿಯ ಗ್ರಾಮೀಣ ಸಣ್ಣ ಉದ್ಯಮಗಳಿಗೆ ಪ್ರದರ್ಶನ ಯಶಸ್ಸಿನ-ದರ ಮತ್ತು ಪ್ರತಿಫಲ ಊಹೆಗಳ ಆಧಾರದ ಮೇಲೆ ಪ್ರೋಟೋಟೈಪ್ ಅಂದಾಜುಗಳಾಗಿವೆ. ಇದು ಲಾಭದ ಖಾತರಿಯಲ್ಲ ಮತ್ತು ಸೂಕ್ತ ವ್ಯವಹಾರ ಯೋಜನೆಗೆ ಪರ್ಯಾಯವಲ್ಲ.",
        "compare_table_title": "ಕೆಲವು ಹೂಡಿಕೆ ಮಟ್ಟಗಳಲ್ಲಿ ಲಾಭ",
        "invest_level": "ಹೂಡಿಕೆ", "invest_benefit": "ಅಂದಾಜು ವಾರ್ಷಿಕ ಲಾಭ ವ್ಯಾಪ್ತಿ",
    },
}
for _lang in TEXT:
    TEXT[_lang].update(EXTRA_TEXT.get(_lang, {}))

# ------------------------------------------------------------
# Complete UI translation layer for dynamic/business screens
# ------------------------------------------------------------
UI_TR = {
    "Hindi": {
        "market_desc":"**{location}** के लिए प्रदर्शन बाज़ार जानकारी। सभी भाव स्थिर नमूना डेटा हैं।",
        "local_suitability":"स्थानीय फसल उपयुक्तता", "no_suitability":"इस स्थान के लिए अभी कोई मेल खाती नमूना फसल उपलब्ध नहीं है।",
        "market_board":"फसल बाज़ार बोर्ड",
        "Business Domain":"व्यवसाय क्षेत्र", "Specific Business":"विशिष्ट व्यवसाय", "Current Location":"वर्तमान स्थान", "Selected in the sidebar":"साइडबार में चुना गया",
        "Select Business":"व्यवसाय चुनें", "Enter Inputs":"जानकारी दर्ज करें", "Strategic Output":"रणनीतिक परिणाम",
        "Step 1 • Select Business":"चरण 1 • व्यवसाय चुनें", "Step 2 • Enter Inputs":"चरण 2 • जानकारी दर्ज करें", "Step 3 • Strategic Output":"चरण 3 • रणनीतिक परिणाम",
        "Step 1 • Business ✓":"चरण 1 • व्यवसाय ✓", "Step 2 • Inputs ✓":"चरण 2 • जानकारी ✓", "Step 3 • Strategic Output":"चरण 3 • रणनीतिक परिणाम",
        "Location & Climate Parameters":"स्थान और जलवायु पैरामीटर", "Soil & Water Profile":"मिट्टी और पानी प्रोफ़ाइल", "Capital & Financial Goals":"पूंजी और वित्तीय लक्ष्य",
        "Use realistic conditions for the specific site and production period. Defaults are regional planning values and should be replaced with measured/current values where available.":"विशिष्ट स्थान और उत्पादन अवधि के लिए वास्तविक परिस्थितियाँ दर्ज करें। डिफ़ॉल्ट क्षेत्रीय योजना मान हैं; जहाँ संभव हो उन्हें वर्तमान माप से बदलें।",
        "Use the latest soil/water information available. Tooltips explain what each field is used for.":"उपलब्ध नवीनतम मिट्टी/पानी की जानकारी दर्ज करें। टूलटिप हर फ़ील्ड का उपयोग समझाता है।",
        "Enter deployable capital, operating capacity and commercial constraints. Unknown or missing fields are excluded from adaptive scoring.":"उपयोग योग्य पूंजी, संचालन क्षमता और व्यावसायिक सीमाएँ दर्ज करें। अज्ञात या खाली फ़ील्ड स्कोर में शामिल नहीं किए जाते।",
        "This activity does not require additional location/climate inputs beyond the selected location.":"इस गतिविधि के लिए चुने गए स्थान के अलावा अतिरिक्त स्थान/जलवायु जानकारी आवश्यक नहीं है।",
        "No separate soil/water profile is required for this activity.":"इस गतिविधि के लिए अलग मिट्टी/पानी प्रोफ़ाइल आवश्यक नहीं है।",
        "No additional financial/setup inputs are required for this activity.":"इस गतिविधि के लिए अतिरिक्त वित्तीय/सेटअप जानकारी आवश्यक नहीं है।",
        "Tip: use the latest available measurements and realistic capacity. The recommendation engine adapts to partial information.":"सुझाव: नवीनतम माप और वास्तविक क्षमता का उपयोग करें। सिफारिश इंजन उपलब्ध जानकारी के अनुसार अपना आकलन बदलता है।",
        "Generate Recommendation":"सिफारिश बनाएं", "Business Recommendation":"व्यवसाय सिफारिश",
        "Select one business activity and enter only the inputs relevant to that activity. The form adapts automatically and missing values are not treated as zero.":"एक व्यवसाय गतिविधि चुनें और केवल उससे संबंधित जानकारी दर्ज करें। फ़ॉर्म अपने आप अनुकूलित होता है और खाली मानों को शून्य नहीं माना जाता।",
        "Choose the broad business domain first.":"पहले व्यापक व्यवसाय क्षेत्र चुनें।", "Choose the exact activity you want to evaluate.":"जिस गतिविधि का आकलन करना है उसे चुनें।",
        "Rule-based feasibility assessment":"नियम-आधारित व्यवहार्यता आकलन", "Financial figures are planning estimates, not guarantees. Validate local supplier quotes, buyer prices and current scheme rules before committing capital.":"वित्तीय आंकड़े केवल योजना अनुमान हैं, गारंटी नहीं। पूंजी लगाने से पहले स्थानीय आपूर्तिकर्ता दर, खरीदार मूल्य और वर्तमान योजना नियम सत्यापित करें।",
        "Species / Variety / Product Selection":"प्रजाति / किस्म / उत्पाद चयन", "Execution Roadmap":"कार्यान्वयन रोडमैप",
        "Prepare → pilot → validate → scale. Each phase has a clear translate_output_recursive(outcome) and a go/no-go translate_output_recursive(gate).":"तैयारी → पायलट → सत्यापन → विस्तार। हर चरण का स्पष्ट परिणाम और आगे बढ़ने का मानदंड है।",
        "Scale rule":"विस्तार नियम", "Practical Decision Check":"व्यावहारिक निर्णय जाँच", "Financial & Success Benchmarks":"वित्तीय और सफलता मानदंड",
        "Applicable scheme information is shown for the selected business mapping. Eligibility and support depend on current official guidelines.":"चयनित व्यवसाय मैपिंग के लिए संबंधित योजना जानकारी दिखाई गई है। पात्रता और सहायता वर्तमान आधिकारिक दिशानिर्देशों पर निर्भर करती है।",
        "":"इस प्रोटोटाइप में इस व्यवसाय के लिए कोई योजना मैप नहीं है। अधिक विकल्पों के लिए सरकारी योजनाएँ देखें।",
        "Generate Business Recommendations":"व्यवसाय सिफारिशें बनाएं",
    },
    "Kannada": {
        "market_desc":"**{location}** ಗಾಗಿ ಪ್ರದರ್ಶನ ಮಾರುಕಟ್ಟೆ ಮಾಹಿತಿ. ಎಲ್ಲಾ ಬೆಲೆಗಳು ಸ್ಥಿರ ಮಾದರಿ ಡೇಟಾ.",
        "local_suitability":"ಸ್ಥಳೀಯ ಬೆಳೆ ಸೂಕ್ತತೆ", "no_suitability":"ಈ ಸ್ಥಳಕ್ಕೆ ಹೊಂದುವ ಮಾದರಿ ಬೆಳೆ ಇನ್ನೂ ಲಭ್ಯವಿಲ್ಲ.", "market_board":"ಬೆಳೆ ಮಾರುಕಟ್ಟೆ ಫಲಕ",
        "Business Domain":"ವ್ಯವಹಾರ ಕ್ಷೇತ್ರ", "Specific Business":"ನಿರ್ದಿಷ್ಟ ವ್ಯವಹಾರ", "Current Location":"ಪ್ರಸ್ತುತ ಸ್ಥಳ", "Selected in the sidebar":"ಸೈಡ್‌ಬಾರ್‌ನಲ್ಲಿ ಆಯ್ಕೆ ಮಾಡಲಾಗಿದೆ",
        "Select Business":"ವ್ಯವಹಾರ ಆಯ್ಕೆ", "Enter Inputs":"ಮಾಹಿತಿ ನಮೂದಿಸಿ", "Strategic Output":"ತಂತ್ರಾತ್ಮಕ ಫಲಿತಾಂಶ",
        "Step 1 • Select Business":"ಹಂತ 1 • ವ್ಯವಹಾರ ಆಯ್ಕೆ", "Step 2 • Enter Inputs":"ಹಂತ 2 • ಮಾಹಿತಿ ನಮೂದಿಸಿ", "Step 3 • Strategic Output":"ಹಂತ 3 • ತಂತ್ರಾತ್ಮಕ ಫಲಿತಾಂಶ",
        "Step 1 • Business ✓":"ಹಂತ 1 • ವ್ಯವಹಾರ ✓", "Step 2 • Inputs ✓":"ಹಂತ 2 • ಮಾಹಿತಿ ✓",
        "Location & Climate Parameters":"ಸ್ಥಳ ಮತ್ತು ಹವಾಮಾನ ನಿಯತಾಂಕಗಳು", "Soil & Water Profile":"ಮಣ್ಣು ಮತ್ತು ನೀರಿನ ಪ್ರೊಫೈಲ್", "Capital & Financial Goals":"ಬಂಡವಾಳ ಮತ್ತು ಹಣಕಾಸು ಗುರಿಗಳು",
        "Use realistic conditions for the specific site and production period. Defaults are regional planning values and should be replaced with measured/current values where available.":"ನಿರ್ದಿಷ್ಟ ಸ್ಥಳ ಮತ್ತು ಉತ್ಪಾದನಾ ಅವಧಿಗೆ ನೈಜ ಪರಿಸ್ಥಿತಿಗಳನ್ನು ನಮೂದಿಸಿ. ಡೀಫಾಲ್ಟ್‌ಗಳು ಪ್ರಾದೇಶಿಕ ಯೋಜನಾ ಮೌಲ್ಯಗಳಾಗಿವೆ; ಸಾಧ್ಯವಾದಲ್ಲಿ ಪ್ರಸ್ತುತ ಮಾಪನಗಳಿಂದ ಬದಲಾಯಿಸಿ.",
        "Use the latest soil/water information available. Tooltips explain what each field is used for.":"ಲಭ್ಯವಿರುವ ಇತ್ತೀಚಿನ ಮಣ್ಣು/ನೀರಿನ ಮಾಹಿತಿಯನ್ನು ಬಳಸಿ. ಟೂಲ್‌ಟಿಪ್‌ಗಳು ಪ್ರತಿಯೊಂದು ಕ್ಷೇತ್ರದ ಬಳಕೆಯನ್ನು ವಿವರಿಸುತ್ತವೆ.",
        "Enter deployable capital, operating capacity and commercial constraints. Unknown or missing fields are excluded from adaptive scoring.":"ಬಳಸಬಹುದಾದ ಬಂಡವಾಳ, ಕಾರ್ಯಾಚರಣಾ ಸಾಮರ್ಥ್ಯ ಮತ್ತು ವ್ಯವಹಾರ ಮಿತಿಗಳನ್ನು ನಮೂದಿಸಿ. ತಿಳಿಯದ ಅಥವಾ ಖಾಲಿ ಕ್ಷೇತ್ರಗಳನ್ನು ಅಂಕದಲ್ಲಿ ಸೇರಿಸಲಾಗುವುದಿಲ್ಲ.",
        "This activity does not require additional location/climate inputs beyond the selected location.":"ಈ ಚಟುವಟಿಕೆಗೆ ಆಯ್ಕೆ ಮಾಡಿದ ಸ್ಥಳದ ಹೊರತಾಗಿ ಹೆಚ್ಚುವರಿ ಸ್ಥಳ/ಹವಾಮಾನ ಮಾಹಿತಿ ಅಗತ್ಯವಿಲ್ಲ.",
        "No separate soil/water profile is required for this activity.":"ಈ ಚಟುವಟಿಕೆಗೆ ಪ್ರತ್ಯೇಕ ಮಣ್ಣು/ನೀರಿನ ಪ್ರೊಫೈಲ್ ಅಗತ್ಯವಿಲ್ಲ.",
        "No additional financial/setup inputs are required for this activity.":"ಈ ಚಟುವಟಿಕೆಗೆ ಹೆಚ್ಚುವರಿ ಹಣಕಾಸು/ಸೆಟಪ್ ಮಾಹಿತಿ ಅಗತ್ಯವಿಲ್ಲ.",
        "Tip: use the latest available measurements and realistic capacity. The recommendation engine adapts to partial information.":"ಸಲಹೆ: ಲಭ್ಯವಿರುವ ಇತ್ತೀಚಿನ ಮಾಪನಗಳು ಮತ್ತು ನೈಜ ಸಾಮರ್ಥ್ಯವನ್ನು ಬಳಸಿ. ಶಿಫಾರಸು ಎಂಜಿನ್ ಲಭ್ಯವಿರುವ ಮಾಹಿತಿಗೆ ಹೊಂದಿಕೊಳ್ಳುತ್ತದೆ.",
        "Generate Recommendation":"ಶಿಫಾರಸು ರಚಿಸಿ", "Business Recommendation":"ವ್ಯವಹಾರ ಶಿಫಾರಸು",
        "Select one business activity and enter only the inputs relevant to that activity. The form adapts automatically and missing values are not treated as zero.":"ಒಂದು ವ್ಯವಹಾರ ಚಟುವಟಿಕೆಯನ್ನು ಆಯ್ಕೆ ಮಾಡಿ ಮತ್ತು ಅದಕ್ಕೆ ಸಂಬಂಧಿಸಿದ ಮಾಹಿತಿಯನ್ನು ಮಾತ್ರ ನಮೂದಿಸಿ. ಫಾರ್ಮ್ ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಹೊಂದಿಕೊಳ್ಳುತ್ತದೆ ಮತ್ತು ಖಾಲಿ ಮೌಲ್ಯಗಳನ್ನು ಶೂನ್ಯವೆಂದು ಪರಿಗಣಿಸಲಾಗುವುದಿಲ್ಲ.",
        "Choose the broad business domain first.":"ಮೊದಲು ವ್ಯಾಪಕ ವ್ಯವಹಾರ ಕ್ಷೇತ್ರವನ್ನು ಆಯ್ಕೆ ಮಾಡಿ.", "Choose the exact activity you want to evaluate.":"ನೀವು ಮೌಲ್ಯಮಾಪನ ಮಾಡಲು ಬಯಸುವ ನಿಖರ ಚಟುವಟಿಕೆಯನ್ನು ಆಯ್ಕೆ ಮಾಡಿ.",
        "Rule-based feasibility assessment":"ನಿಯಮಾಧಾರಿತ ಕಾರ್ಯಸಾಧ್ಯತಾ ಮೌಲ್ಯಮಾಪನ", "Financial figures are planning estimates, not guarantees. Validate local supplier quotes, buyer prices and current scheme rules before committing capital.":"ಹಣಕಾಸು ಅಂಕಿಅಂಶಗಳು ಯೋಜನಾ ಅಂದಾಜುಗಳು ಮಾತ್ರ, ಖಾತರಿಗಳಲ್ಲ. ಬಂಡವಾಳ ಹೂಡಿಕೆಗೂ ಮೊದಲು ಸ್ಥಳೀಯ ಪೂರೈಕೆದಾರರ ದರ, ಖರೀದಿದಾರರ ಬೆಲೆ ಮತ್ತು ಪ್ರಸ್ತುತ ಯೋಜನಾ ನಿಯಮಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.",
        "Species / Variety / Product Selection":"ಜಾತಿ / ತಳಿ / ಉತ್ಪನ್ನ ಆಯ್ಕೆ", "Execution Roadmap":"ಕಾರ್ಯಗತಗೊಳಿಸುವಿಕೆ ಮಾರ್ಗಸೂಚಿ",
        "Prepare → pilot → validate → scale. Each phase has a clear translate_output_recursive(outcome) and a go/no-go translate_output_recursive(gate).":"ತಯಾರಿ → ಪೈಲಟ್ → ಪರಿಶೀಲನೆ → ವಿಸ್ತರಣೆ. ಪ್ರತಿ ಹಂತಕ್ಕೂ ಸ್ಪಷ್ಟ ಫಲಿತಾಂಶ ಮತ್ತು ಮುಂದುವರಿಯುವ ಮಾನದಂಡವಿದೆ.",
        "Scale rule":"ವಿಸ್ತರಣೆ ನಿಯಮ", "Practical Decision Check":"ಪ್ರಾಯೋಗಿಕ ನಿರ್ಧಾರ ಪರಿಶೀಲನೆ", "Financial & Success Benchmarks":"ಹಣಕಾಸು ಮತ್ತು ಯಶಸ್ಸಿನ ಮಾನದಂಡಗಳು",
        "Applicable scheme information is shown for the selected business mapping. Eligibility and support depend on current official guidelines.":"ಆಯ್ಕೆ ಮಾಡಿದ ವ್ಯವಹಾರ ಮ್ಯಾಪಿಂಗ್‌ಗೆ ಸಂಬಂಧಿಸಿದ ಯೋಜನಾ ಮಾಹಿತಿಯನ್ನು ತೋರಿಸಲಾಗಿದೆ. ಅರ್ಹತೆ ಮತ್ತು ನೆರವು ಪ್ರಸ್ತುತ ಅಧಿಕೃತ ಮಾರ್ಗಸೂಚಿಗಳ ಮೇಲೆ ಅವಲಂಬಿತವಾಗಿದೆ.",
        "":"ಈ ಪ್ರೋಟೋಟೈಪ್‌ನಲ್ಲಿ ಈ ವ್ಯವಹಾರಕ್ಕೆ ಯಾವುದೇ ಯೋಜನೆ ಮ್ಯಾಪ್ ಮಾಡಲಾಗಿಲ್ಲ. ಹೆಚ್ಚಿನ ಆಯ್ಕೆಗಳಿಗಾಗಿ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳನ್ನು ನೋಡಿ.",
        "Generate Business Recommendations":"ವ್ಯವಹಾರ ಶಿಫಾರಸುಗಳನ್ನು ರಚಿಸಿ",
    }
}

for _lang in TEXT:
    TEXT[_lang].update(UI_TR.get(_lang, {}))

# ------------------------------------------------------------
# COMPLETE UI FALLBACK TRANSLATOR
# ------------------------------------------------------------
# Some business profiles contain labels/options/descriptions directly in
# the configuration.  The dictionaries above cover the main UI, but this
# fallback also translates those dynamic strings so changing the language
# affects the whole application, not only the navigation.
UI_WORD_TR = {
    "Hindi": {
        "Business Domain":"व्यवसाय क्षेत्र","Specific Business":"विशिष्ट व्यवसाय",
        "Current Location":"वर्तमान स्थान","Selected in the sidebar":"साइडबार में चुना गया",
        "Location & Climate Parameters":"स्थान और जलवायु पैरामीटर","Soil & Water Profile":"मिट्टी और पानी प्रोफ़ाइल",
        "Capital & Financial Goals":"पूंजी और वित्तीय लक्ष्य","Generate Recommendation":"सुझाव तैयार करें",
        "Business Recommendation":"व्यवसाय सुझाव","Select one business activity and enter only the inputs relevant to that activity. The form adapts automatically and missing values are not treated as zero.":"एक व्यवसाय गतिविधि चुनें और केवल उससे संबंधित जानकारी दर्ज करें। फॉर्म अपने आप अनुकूलित होता है और खाली मानों को शून्य नहीं माना जाता।",
        "Step 1 • Select Business":"चरण 1 • व्यवसाय चुनें","Step 2 • Enter Inputs":"चरण 2 • जानकारी दर्ज करें","Step 3 • Strategic Output":"चरण 3 • रणनीतिक परिणाम",
        "Step 1 • Business ✓":"चरण 1 • व्यवसाय ✓","Step 2 • Inputs ✓":"चरण 2 • जानकारी ✓",
        "Choose the broad business domain first.":"पहले व्यापक व्यवसाय क्षेत्र चुनें।","Choose the exact activity you want to evaluate.":"वह सटीक गतिविधि चुनें जिसका आकलन करना है।",
        "Use realistic conditions for the specific site and production period. Defaults are regional planning values and should be replaced with measured/current values where available.":"विशिष्ट स्थान और उत्पादन अवधि के लिए वास्तविक परिस्थितियाँ दर्ज करें। डिफ़ॉल्ट क्षेत्रीय योजना मान हैं; जहाँ उपलब्ध हों वहाँ मापे गए या वर्तमान मानों से बदलें।",
        "Use the latest soil/water information available. Tooltips explain what each field is used for.":"उपलब्ध नवीनतम मिट्टी/पानी की जानकारी का उपयोग करें। टूलटिप में बताया गया है कि प्रत्येक फ़ील्ड का उपयोग किसलिए है।",
        "Enter deployable capital, operating capacity and commercial constraints. Unknown or missing fields are excluded from adaptive scoring.":"उपलब्ध पूंजी, संचालन क्षमता और व्यावसायिक सीमाएँ दर्ज करें। अज्ञात या खाली फ़ील्ड अनुकूलित स्कोर में शामिल नहीं किए जाते।",
        "This activity does not require additional location/climate inputs beyond the selected location.":"इस गतिविधि के लिए चुने गए स्थान के अलावा अतिरिक्त स्थान/जलवायु जानकारी आवश्यक नहीं है।",
        "No separate soil/water profile is required for this activity.":"इस गतिविधि के लिए अलग मिट्टी/पानी प्रोफ़ाइल आवश्यक नहीं है।",
        "No additional financial/setup inputs are required for this activity.":"इस गतिविधि के लिए अतिरिक्त वित्तीय/सेटअप जानकारी आवश्यक नहीं है।",
        "Tip: use the latest available measurements and realistic capacity. The recommendation engine adapts to partial information.":"सुझाव: उपलब्ध नवीनतम माप और वास्तविक क्षमता का उपयोग करें। सुझाव इंजन अधूरी जानकारी के अनुसार अनुकूलित होता है।",
        "CAPEX Required":"आवश्यक CAPEX","Break-Even Timeline":"ब्रेक-ईवन समयसीमा","Feasibility Score":"व्यवहार्यता स्कोर","Monthly Operating Cost":"मासिक संचालन लागत",
        "Current input / configured estimate":"वर्तमान जानकारी / कॉन्फ़िगर किया गया अनुमान","Indicative model estimate":"संकेतात्मक मॉडल अनुमान","Adaptive score from available inputs":"उपलब्ध जानकारी से अनुकूलित स्कोर","Indicative, scale-dependent":"संकेतात्मक, पैमाने पर निर्भर",
        "Market & Advisory":"बाज़ार और मार्गदर्शन","Risk Control":"जोखिम नियंत्रण","Financial Benchmarks":"वित्तीय मानदंड",
        "Species / Variety / Product Selection":"प्रजाति / किस्म / उत्पाद चयन","Execution Roadmap":"कार्यान्वयन रोडमैप",
        "Financial figures are planning estimates, not guarantees. Validate local supplier quotes, buyer prices and current scheme rules before committing capital.":"वित्तीय आंकड़े केवल योजना अनुमान हैं, गारंटी नहीं। पूंजी लगाने से पहले स्थानीय आपूर्तिकर्ता दर, खरीदार कीमत और वर्तमान योजना नियमों की पुष्टि करें।",
        "Priority gaps":"प्राथमिकता अंतराल","Practical Decision Check":"व्यावहारिक निर्णय जाँच",
        "":"इस प्रोटोटाइप में इस व्यवसाय से कोई योजना मैप नहीं की गई है। अधिक योजनाओं के लिए सरकारी योजनाएँ देखें।",
        "Do not move straight from setup to full investment. Validate the pilot first.":"सेटअप से सीधे पूर्ण निवेश पर न जाएँ। पहले पायलट को सत्यापित करें।",
        "Selection":"चयन","Schemes":"योजनाएँ","Market":"बाज़ार","Advisory":"मार्गदर्शन",
        "Input":"इनपुट","Output":"परिणाम","Score":"स्कोर","Reason":"कारण","Action":"कार्रवाई",
        "No":"नहीं","Yes":"हाँ","Some":"कुछ","Intermediate":"मध्यम","Unknown":"अज्ञात",
        "Cows":"गाय","Buffaloes":"भैंस","Mixed":"मिश्रित","Existing pond":"मौजूदा तालाब","New pond":"नया तालाब","Lined pond":"लाइनिंग वाला तालाब",
        "Canal":"नहर","Borewell":"बोरवेल","Tank/Pond":"टैंक/तालाब","River":"नदी","Seasonal":"मौसमी","Perennial":"सालभर उपलब्ध",
        "Cereals":"अनाज","Pulses":"दलहन","Oilseeds":"तिलहन","Commercial Crops":"व्यावसायिक फसलें","Allied Activities":"संबंधित गतिविधियाँ",
        "Land":"भूमि","Water":"पानी","Soil":"मिट्टी","Market":"बाज़ार","Equipment":"उपकरण","Packaging":"पैकेजिंग",
        "Processing":"प्रसंस्करण","Storage":"भंडारण","Transport":"परिवहन","Workspace":"कार्यस्थल","Workshop":"कार्यशाला",
        "Demand":"मांग","Experience":"अनुभव","Labour":"श्रमिक","Capital":"पूंजी","Investment":"निवेश","Electricity":"बिजली",
        "Feed":"चारा","Fuel":"ईंधन","Vehicle":"वाहन","Operator":"ऑपरेटर","Driver":"चालक","Skill":"कौशल",
        "Temperature":"तापमान","Humidity":"आर्द्रता","Rainfall":"वर्षा","Irrigation":"सिंचाई","Season":"मौसम",
        "Poor":"कमज़ोर","Moderate":"मध्यम","Good":"अच्छा","Low":"कम","Medium":"मध्यम","High":"अधिक","Limited":"सीमित","Partial":"आंशिक","Available":"उपलब्ध","Reliable":"विश्वसनीय","Shared":"साझा",
        "Beginner":"शुरुआती","Some experience":"कुछ अनुभव","Experienced":"अनुभवी",
        "Within 3 months":"3 महीने के भीतर","3–6 months":"3–6 महीने","6–12 months":"6–12 महीने","12+ months":"12+ महीने",
        "Rain-fed":"वर्षा आधारित","None":"नहीं","Other":"अन्य","Two-wheeler":"दो पहिया वाहन","Auto/three-wheeler":"ऑटो/तीन पहिया वाहन","Pickup":"पिकअप","Mini truck":"मिनी ट्रक","Leased":"लीज़ पर",
        "Agriculture":"कृषि","Livestock":"पशुपालन","Aquaculture":"मत्स्य पालन","Food Processing":"खाद्य प्रसंस्करण","Services":"सेवाएँ","Retail":"खुदरा",
        "Crop Cultivation":"फसल खेती","Vegetable Cultivation":"सब्ज़ी खेती","Fruit Cultivation":"फल खेती","Spice Cultivation":"मसाला खेती","Floriculture":"फूलों की खेती",
        "Poultry Farming":"पोल्ट्री फार्मिंग","Dairy Farming":"डेयरी फार्मिंग","Goat Farming":"बकरी पालन","Sheep Farming":"भेड़ पालन","Fish Farming":"मछली पालन",
    },
    "Kannada": {
        "Business Domain":"ವ್ಯವಹಾರ ಕ್ಷೇತ್ರ","Specific Business":"ನಿರ್ದಿಷ್ಟ ವ್ಯವಹಾರ","Current Location":"ಪ್ರಸ್ತುತ ಸ್ಥಳ","Selected in the sidebar":"ಸೈಡ್‌ಬಾರ್‌ನಲ್ಲಿ ಆಯ್ಕೆ ಮಾಡಲಾಗಿದೆ",
        "Location & Climate Parameters":"ಸ್ಥಳ ಮತ್ತು ಹವಾಮಾನ ನಿಯತಾಂಕಗಳು","Soil & Water Profile":"ಮಣ್ಣು ಮತ್ತು ನೀರಿನ ಪ್ರೊಫೈಲ್","Capital & Financial Goals":"ಬಂಡವಾಳ ಮತ್ತು ಹಣಕಾಸಿನ ಗುರಿಗಳು","Generate Recommendation":"ಶಿಫಾರಸು ರಚಿಸಿ",
        "Business Recommendation":"ವ್ಯವಹಾರ ಶಿಫಾರಸು","Step 1 • Select Business":"ಹಂತ 1 • ವ್ಯವಹಾರ ಆಯ್ಕೆ","Step 2 • Enter Inputs":"ಹಂತ 2 • ಮಾಹಿತಿ ನಮೂದಿಸಿ","Step 3 • Strategic Output":"ಹಂತ 3 • ತಂತ್ರಾತ್ಮಕ ಫಲಿತಾಂಶ",
        "Step 1 • Business ✓":"ಹಂತ 1 • ವ್ಯವಹಾರ ✓","Step 2 • Inputs ✓":"ಹಂತ 2 • ಮಾಹಿತಿ ✓",
        "Choose the broad business domain first.":"ಮೊದಲು ವ್ಯಾಪಕ ವ್ಯವಹಾರ ಕ್ಷೇತ್ರವನ್ನು ಆಯ್ಕೆಮಾಡಿ.","Choose the exact activity you want to evaluate.":"ಮೌಲ್ಯಮಾಪನ ಮಾಡಲು ಬಯಸುವ ನಿಖರ ಚಟುವಟಿಕೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ.",
        "Use realistic conditions for the specific site and production period. Defaults are regional planning values and should be replaced with measured/current values where available.":"ನಿರ್ದಿಷ್ಟ ಸ್ಥಳ ಮತ್ತು ಉತ್ಪಾದನಾ ಅವಧಿಗೆ ವಾಸ್ತವಿಕ ಪರಿಸ್ಥಿತಿಗಳನ್ನು ನಮೂದಿಸಿ. ಡೀಫಾಲ್ಟ್‌ಗಳು ಪ್ರಾದೇಶಿಕ ಯೋಜನಾ ಮೌಲ್ಯಗಳಾಗಿವೆ; ಲಭ್ಯವಿದ್ದಲ್ಲಿ ಪ್ರಸ್ತುತ/ಅಳತೆ ಮಾಡಿದ ಮೌಲ್ಯಗಳಿಂದ ಬದಲಿಸಿ.",
        "Use the latest soil/water information available. Tooltips explain what each field is used for.":"ಲಭ್ಯವಿರುವ ಇತ್ತೀಚಿನ ಮಣ್ಣು/ನೀರಿನ ಮಾಹಿತಿಯನ್ನು ಬಳಸಿ. ಪ್ರತಿಯೊಂದು ಕ್ಷೇತ್ರದ ಬಳಕೆಯನ್ನು ಟೂಲ್‌ಟಿಪ್ ವಿವರಿಸುತ್ತದೆ.",
        "Enter deployable capital, operating capacity and commercial constraints. Unknown or missing fields are excluded from adaptive scoring.":"ಬಳಸಬಹುದಾದ ಬಂಡವಾಳ, ಕಾರ್ಯಾಚರಣಾ ಸಾಮರ್ಥ್ಯ ಮತ್ತು ವಾಣಿಜ್ಯ ಮಿತಿಗಳನ್ನು ನಮೂದಿಸಿ. ತಿಳಿಯದ ಅಥವಾ ಖಾಲಿ ಕ್ಷೇತ್ರಗಳನ್ನು ಹೊಂದಿಕೊಳ್ಳುವ ಅಂಕದಲ್ಲಿ ಸೇರಿಸಲಾಗುವುದಿಲ್ಲ.",
        "This activity does not require additional location/climate inputs beyond the selected location.":"ಆಯ್ಕೆ ಮಾಡಿದ ಸ್ಥಳದ ಹೊರತಾಗಿ ಈ ಚಟುವಟಿಕೆಗೆ ಹೆಚ್ಚುವರಿ ಸ್ಥಳ/ಹವಾಮಾನ ಮಾಹಿತಿ ಅಗತ್ಯವಿಲ್ಲ.",
        "No separate soil/water profile is required for this activity.":"ಈ ಚಟುವಟಿಕೆಗೆ ಪ್ರತ್ಯೇಕ ಮಣ್ಣು/ನೀರಿನ ಪ್ರೊಫೈಲ್ ಅಗತ್ಯವಿಲ್ಲ.",
        "No additional financial/setup inputs are required for this activity.":"ಈ ಚಟುವಟಿಕೆಗೆ ಹೆಚ್ಚುವರಿ ಹಣಕಾಸು/ಸೆಟಪ್ ಮಾಹಿತಿ ಅಗತ್ಯವಿಲ್ಲ.",
        "Tip: use the latest available measurements and realistic capacity. The recommendation engine adapts to partial information.":"ಸಲಹೆ: ಲಭ್ಯವಿರುವ ಇತ್ತೀಚಿನ ಅಳತೆಗಳು ಮತ್ತು ವಾಸ್ತವಿಕ ಸಾಮರ್ಥ್ಯವನ್ನು ಬಳಸಿ. ಶಿಫಾರಸು ಎಂಜಿನ್ ಅಪೂರ್ಣ ಮಾಹಿತಿಗೆ ಹೊಂದಿಕೊಳ್ಳುತ್ತದೆ.",
        "CAPEX Required":"ಅಗತ್ಯ CAPEX","Break-Even Timeline":"ಬ್ರೇಕ್-ಈವನ್ ಸಮಯಪಟ್ಟಿ","Feasibility Score":"ಕಾರ್ಯಸಾಧ್ಯತಾ ಅಂಕ","Monthly Operating Cost":"ಮಾಸಿಕ ಕಾರ್ಯಾಚರಣಾ ವೆಚ್ಚ",
        "Current input / configured estimate":"ಪ್ರಸ್ತುತ ಮಾಹಿತಿ / ಕಾನ್ಫಿಗರ್ ಮಾಡಿದ ಅಂದಾಜು","Indicative model estimate":"ಸೂಚಕ ಮಾದರಿ ಅಂದಾಜು","Adaptive score from available inputs":"ಲಭ್ಯ ಮಾಹಿತಿಯಿಂದ ಹೊಂದಿಕೊಳ್ಳುವ ಅಂಕ","Indicative, scale-dependent":"ಸೂಚಕ, ಪ್ರಮಾಣದ ಮೇಲೆ ಅವಲಂಬಿತ",
        "Market & Advisory":"ಮಾರುಕಟ್ಟೆ ಮತ್ತು ಮಾರ್ಗದರ್ಶನ","Risk Control":"ಅಪಾಯ ನಿಯಂತ್ರಣ","Financial Benchmarks":"ಹಣಕಾಸು ಮಾನದಂಡಗಳು",
        "Species / Variety / Product Selection":"ಜಾತಿ / ತಳಿ / ಉತ್ಪನ್ನ ಆಯ್ಕೆ","Execution Roadmap":"ಕಾರ್ಯಗತಗೊಳಿಸುವಿಕೆ ಮಾರ್ಗಸೂಚಿ",
        "Selection":"ಆಯ್ಕೆ","Schemes":"ಯೋಜನೆಗಳು","Market":"ಮಾರುಕಟ್ಟೆ","Advisory":"ಮಾರ್ಗದರ್ಶನ","Input":"ಇನ್‌ಪುಟ್","Output":"ಫಲಿತಾಂಶ","Score":"ಅಂಕ","Reason":"ಕಾರಣ","Action":"ಕ್ರಮ",
        "No":"ಇಲ್ಲ","Yes":"ಹೌದು","Some":"ಕೆಲವು","Intermediate":"ಮಧ್ಯಮ","Unknown":"ತಿಳಿದಿಲ್ಲ",
        "Cows":"ಹಸುಗಳು","Buffaloes":"ಎಮ್ಮೆಗಳು","Mixed":"ಮಿಶ್ರ","Existing pond":"ಅಸ್ತಿತ್ವದಲ್ಲಿರುವ ಕೆರೆ","New pond":"ಹೊಸ ಕೆರೆ","Lined pond":"ಲೈನಿಂಗ್ ಮಾಡಿದ ಕೆರೆ",
        "Canal":"ಕಾಲುವೆ","Borewell":"ಬೋರ್‌ವೆಲ್","Tank/Pond":"ಟ್ಯಾಂಕ್/ಕೆರೆ","River":"ನದಿ","Seasonal":"ಋತುಮಾನ","Perennial":"ವರ್ಷಪೂರ್ತಿ",
        "Cereals":"ಧಾನ್ಯಗಳು","Pulses":"ಬೇಳೆಕಾಳುಗಳು","Oilseeds":"ಎಣ್ಣೆಬೀಜಗಳು","Commercial Crops":"ವಾಣಿಜ್ಯ ಬೆಳೆಗಳು","Allied Activities":"ಸಂಬಂಧಿತ ಚಟುವಟಿಕೆಗಳು",
        "Land":"ಭೂಮಿ","Water":"ನೀರು","Soil":"ಮಣ್ಣು","Equipment":"ಉಪಕರಣ","Packaging":"ಪ್ಯಾಕೇಜಿಂಗ್","Processing":"ಸಂಸ್ಕರಣೆ","Storage":"ಸಂಗ್ರಹಣೆ","Transport":"ಸಾರಿಗೆ","Workspace":"ಕಾರ್ಯಸ್ಥಳ","Workshop":"ಕಾರ್ಯಾಗಾರ",
        "Demand":"ಬೇಡಿಕೆ","Experience":"ಅನುಭವ","Labour":"ಕಾರ್ಮಿಕರು","Capital":"ಬಂಡವಾಳ","Investment":"ಹೂಡಿಕೆ","Electricity":"ವಿದ್ಯುತ್","Feed":"ಮೇವು","Fuel":"ಇಂಧನ","Vehicle":"ವಾಹನ","Operator":"ಆಪರೇಟರ್","Driver":"ಚಾಲಕ","Skill":"ಕೌಶಲ್ಯ",
        "Temperature":"ತಾಪಮಾನ","Humidity":"ಆರ್ದ್ರತೆ","Rainfall":"ಮಳೆ","Irrigation":"ನೀರಾವರಿ","Season":"ಋತು",
        "Poor":"ಕಡಿಮೆ","Moderate":"ಮಧ್ಯಮ","Good":"ಉತ್ತಮ","Low":"ಕಡಿಮೆ","Medium":"ಮಧ್ಯಮ","High":"ಹೆಚ್ಚು","Limited":"ಸೀಮಿತ","Partial":"ಭಾಗಶಃ","Available":"ಲಭ್ಯ","Reliable":"ವಿಶ್ವಾಸಾರ್ಹ","Shared":"ಹಂಚಿಕೆ",
        "Beginner":"ಆರಂಭಿಕ","Some experience":"ಸ್ವಲ್ಪ ಅನುಭವ","Experienced":"ಅನುಭವ ಹೊಂದಿರುವವರು",
        "Within 3 months":"3 ತಿಂಗಳೊಳಗೆ","3–6 months":"3–6 ತಿಂಗಳು","6–12 months":"6–12 ತಿಂಗಳು","12+ months":"12+ ತಿಂಗಳು",
        "Rain-fed":"ಮಳೆ ಆಧಾರಿತ","None":"ಇಲ್ಲ","Other":"ಇತರೆ","Two-wheeler":"ದ್ವಿಚಕ್ರ ವಾಹನ","Auto/three-wheeler":"ಆಟೋ/ಮೂರು ಚಕ್ರ ವಾಹನ","Pickup":"ಪಿಕಪ್","Mini truck":"ಮಿನಿ ಟ್ರಕ್","Leased":"ಲೀಸ್‌ಗೆ",
        "Agriculture":"ಕೃಷಿ","Livestock":"ಪಶುಸಂಗೋಪನೆ","Aquaculture":"ಮೀನುಗಾರಿಕೆ","Food Processing":"ಆಹಾರ ಸಂಸ್ಕರಣೆ","Services":"ಸೇವೆಗಳು","Retail":"ಚಿಲ್ಲರೆ",
        "Crop Cultivation":"ಬೆಳೆ ಕೃಷಿ","Vegetable Cultivation":"ತರಕಾರಿ ಕೃಷಿ","Fruit Cultivation":"ಹಣ್ಣು ಕೃಷಿ","Spice Cultivation":"ಮಸಾಲೆ ಕೃಷಿ","Floriculture":"ಹೂ ಬೆಳೆ",
        "Poultry Farming":"ಕೋಳಿ ಸಾಕಣೆ","Dairy Farming":"ಹೈನುಗಾರಿಕೆ","Goat Farming":"ಮೇಕೆ ಸಾಕಣೆ","Sheep Farming":"ಕುರಿ ಸಾಕಣೆ","Fish Farming":"ಮೀನು ಸಾಕಣೆ",
    }
}


# Agriculture/environment field translations (including NPK inputs and helper text).
ENV_UI_TR = {
    "Hindi": {
        "Nitrogen (N)":"नाइट्रोजन (N)", "Phosphorus (P)":"फॉस्फोरस (P)", "Potassium (K)":"पोटैशियम (K)",
        "Temperature (°C)":"तापमान (°C)", "Humidity (%)":"आर्द्रता (%)", "Soil pH":"मिट्टी का pH", "Rainfall (mm)":"वर्षा (मिमी)",
        "Nitrogen":"नाइट्रोजन", "Phosphorus":"फॉस्फोरस", "Potassium":"पोटैशियम",
        "Soil pH":"मिट्टी का pH", "Water availability":"पानी की उपलब्धता", "Market access":"बाज़ार तक पहुँच",
        "Feed availability":"चारे की उपलब्धता", "Fodder availability":"पशु चारे की उपलब्धता", "Veterinary access":"पशु चिकित्सा सुविधा",
        "Housing/shed":"आवास/शेड", "Grazing/feed availability":"चराई/चारे की उपलब्धता", "Electricity":"बिजली",
        "Use the latest soil-test N value; this helps compare crop requirements.":"मिट्टी की नवीनतम जाँच में दिया गया N मान दर्ज करें; इससे फसल की आवश्यकता की तुलना करने में मदद मिलती है।",
        "Use the latest soil-test P value.":"मिट्टी की नवीनतम जाँच में दिया गया P मान दर्ज करें।",
        "Use the latest soil-test K value.":"मिट्टी की नवीनतम जाँच में दिया गया K मान दर्ज करें।",
        "Use the latest soil-test pH; most crops have a preferred pH band.":"मिट्टी की नवीनतम जाँच का pH मान दर्ज करें; अधिकांश फसलों के लिए एक उपयुक्त pH सीमा होती है।",
        "Enter the expected temperature during the production period.":"उत्पादन अवधि के दौरान अपेक्षित तापमान दर्ज करें।",
        "Enter typical relative humidity for the production area.":"उत्पादन क्षेत्र की सामान्य सापेक्ष आर्द्रता दर्ज करें।",
        "Enter expected seasonal rainfall or the relevant production-period value.":"अपेक्षित मौसमी वर्षा या उत्पादन अवधि का संबंधित मान दर्ज करें।",
        "Enter a practical value":"व्यावहारिक मान दर्ज करें",
    },
    "Kannada": {
        "Nitrogen (N)":"ನೈಟ್ರೋಜನ್ (N)", "Phosphorus (P)":"ಫಾಸ್ಫರಸ್ (P)", "Potassium (K)":"ಪೊಟ್ಯಾಸಿಯಮ್ (K)",
        "Temperature (°C)":"ತಾಪಮಾನ (°C)", "Humidity (%)":"ಆರ್ದ್ರತೆ (%)", "Soil pH":"ಮಣ್ಣಿನ pH", "Rainfall (mm)":"ಮಳೆ (ಮಿಮೀ)",
        "Nitrogen":"ನೈಟ್ರೋಜನ್", "Phosphorus":"ಫಾಸ್ಫರಸ್", "Potassium":"ಪೊಟ್ಯಾಸಿಯಮ್",
        "Water availability":"ನೀರಿನ ಲಭ್ಯತೆ", "Market access":"ಮಾರುಕಟ್ಟೆ ಪ್ರವೇಶ", "Feed availability":"ಮೇವು ಲಭ್ಯತೆ",
        "Fodder availability":"ಪಶು ಮೇವು ಲಭ್ಯತೆ", "Veterinary access":"ಪಶುವೈದ್ಯಕೀಯ ಸೌಲಭ್ಯ", "Housing/shed":"ವಸತಿ/ಶೆಡ್",
        "Grazing/feed availability":"ಮೇಯಿಸುವಿಕೆ/ಮೇವು ಲಭ್ಯತೆ", "Electricity":"ವಿದ್ಯುತ್",
        "Use the latest soil-test N value; this helps compare crop requirements.":"ಇತ್ತೀಚಿನ ಮಣ್ಣಿನ ಪರೀಕ್ಷೆಯ N ಮೌಲ್ಯವನ್ನು ನಮೂದಿಸಿ; ಇದು ಬೆಳೆ ಅಗತ್ಯಗಳನ್ನು ಹೋಲಿಸಲು ಸಹಾಯ ಮಾಡುತ್ತದೆ.",
        "Use the latest soil-test P value.":"ಇತ್ತೀಚಿನ ಮಣ್ಣಿನ ಪರೀಕ್ಷೆಯ P ಮೌಲ್ಯವನ್ನು ನಮೂದಿಸಿ.",
        "Use the latest soil-test K value.":"ಇತ್ತೀಚಿನ ಮಣ್ಣಿನ ಪರೀಕ್ಷೆಯ K ಮೌಲ್ಯವನ್ನು ನಮೂದಿಸಿ.",
        "Use the latest soil-test pH; most crops have a preferred pH band.":"ಇತ್ತೀಚಿನ ಮಣ್ಣಿನ ಪರೀಕ್ಷೆಯ pH ಮೌಲ್ಯವನ್ನು ನಮೂದಿಸಿ; ಹೆಚ್ಚಿನ ಬೆಳೆಗಳಿಗೆ ಸೂಕ್ತ pH ಮಿತಿ ಇರುತ್ತದೆ.",
        "Enter the expected temperature during the production period.":"ಉತ್ಪಾದನಾ ಅವಧಿಯಲ್ಲಿ ನಿರೀಕ್ಷಿತ ತಾಪಮಾನವನ್ನು ನಮೂದಿಸಿ.",
        "Enter typical relative humidity for the production area.":"ಉತ್ಪಾದನಾ ಪ್ರದೇಶದ ಸಾಮಾನ್ಯ ಸಾಪೇಕ್ಷ ಆರ್ದ್ರತೆಯನ್ನು ನಮೂದಿಸಿ.",
        "Enter expected seasonal rainfall or the relevant production-period value.":"ನಿರೀಕ್ಷಿತ ಋತುಮಾನದ ಮಳೆ ಅಥವಾ ಉತ್ಪಾದನಾ ಅವಧಿಯ ಸಂಬಂಧಿತ ಮೌಲ್ಯವನ್ನು ನಮೂದಿಸಿ.",
        "Enter a practical value":"ಪ್ರಾಯೋಗಿಕ ಮೌಲ್ಯವನ್ನು ನಮೂದಿಸಿ",
    }
}


OUTPUT_TR = {'Hindi': {'Rule-based feasibility assessment': 'नियम-आधारित व्यवहार्यता मूल्यांकन', 'High Risk': 'उच्च जोखिम', 'Medium Risk': 'मध्यम जोखिम', 'Low Risk': 'कम जोखिम', 'Risk': 'जोखिम', 'Level': 'स्तर', 'Impact': 'प्रभाव', 'Control / mitigation': 'नियंत्रण / जोखिम कम करने का उपाय', 'Category': 'श्रेणी', 'Option': 'विकल्प', 'Cycle': 'चक्र', 'Soil / space': 'मिट्टी / स्थान', 'Water': 'पानी', 'Indicative production': 'अनुमानित उत्पादन', 'Specific option': 'विशिष्ट विकल्प', 'Production cycle': 'उत्पादन चक्र', 'Space requirement': 'स्थान की आवश्यकता', 'Climate compatibility': 'जलवायु अनुकूलता', 'Target market': 'लक्षित बाज़ार', 'Execution Roadmap': 'कार्यान्वयन रोडमैप', 'Foundation & Setup': 'आधार और स्थापना', 'READY THE BUSINESS': 'व्यवसाय को तैयार करें', 'Procure & Pilot': 'खरीद और पायलट', 'TEST BEFORE SCALE': 'विस्तार से पहले परीक्षण करें', 'Production, Market & Scale': 'उत्पादन, बाज़ार और विस्तार', 'TURN THE PILOT INTO A BUSINESS': 'पायलट को व्यवसाय में बदलें', 'Outcome:': 'परिणाम:', 'Scale rule': 'विस्तार नियम', 'Route': 'मार्ग', 'Practical use': 'व्यावहारिक उपयोग', 'Pricing focus': 'मूल्य निर्धारण पर ध्यान', 'Differentiation': 'विशेषता', 'Priority gaps': 'प्राथमिक कमियाँ', 'Gap': 'कमी', 'Action': 'कार्रवाई', 'Financial Benchmarks': 'वित्तीय मानदंड', 'Benchmark': 'मानदंड', 'Indicative value': 'अनुमानित मूल्य', 'Interpretation': 'व्याख्या', 'Minimum configured investment': 'न्यूनतम निर्धारित निवेश', 'Planned investment': 'नियोजित निवेश', 'Monthly operating cost': 'मासिक संचालन लागत', 'Annual benefit': 'वार्षिक लाभ', 'Break-even': 'ब्रेक-ईवन', 'Feasibility indicator': 'व्यवहार्यता संकेतक', 'Value': 'मूल्य', 'Note': 'टिप्पणी', 'Scheme': 'योजना', 'What it supports': 'यह किसका समर्थन करती है', 'Financial assistance': 'वित्तीय सहायता', 'Eligibility': 'पात्रता', 'Key documents / conditions': 'मुख्य दस्तावेज़ / शर्तें', 'Practical Decision Check': 'व्यावहारिक निर्णय जाँच', 'Not estimated': 'अनुमान उपलब्ध नहीं', 'Not provided': 'प्रदान नहीं किया गया', 'Not available': 'उपलब्ध नहीं', 'Indicative; verify locally': 'अनुमानित; स्थानीय रूप से सत्यापित करें', 'Current input / configured estimate': 'वर्तमान इनपुट / निर्धारित अनुमान', 'Indicative model estimate': 'अनुमानित मॉडल मूल्य', 'Adaptive score from available inputs': 'उपलब्ध इनपुट से अनुकूलित स्कोर', 'Indicative, scale-dependent': 'अनुमानित, पैमाने पर निर्भर', 'identified': 'पहचाना गया', 'item(s)': 'आइटम', 'Selection': 'चयन', 'Market & Advisory': 'बाज़ार और सलाह', 'Risk Control': 'जोखिम नियंत्रण', 'Schemes': 'योजनाएँ'}, 'Kannada': {'Rule-based feasibility assessment': 'ನಿಯಮ-ಆಧಾರಿತ ಕಾರ್ಯಸಾಧ್ಯತೆ ಮೌಲ್ಯಮಾಪನ', 'High Risk': 'ಹೆಚ್ಚಿನ ಅಪಾಯ', 'Medium Risk': 'ಮಧ್ಯಮ ಅಪಾಯ', 'Low Risk': 'ಕಡಿಮೆ ಅಪಾಯ', 'Risk': 'ಅಪಾಯ', 'Level': 'ಮಟ್ಟ', 'Impact': 'ಪರಿಣಾಮ', 'Control / mitigation': 'ನಿಯಂತ್ರಣ / ಅಪಾಯ ಕಡಿತ ಕ್ರಮ', 'Category': 'ವರ್ಗ', 'Option': 'ಆಯ್ಕೆ', 'Cycle': 'ಚಕ್ರ', 'Soil / space': 'ಮಣ್ಣು / ಸ್ಥಳ', 'Water': 'ನೀರು', 'Indicative production': 'ಅಂದಾಜು ಉತ್ಪಾದನೆ', 'Specific option': 'ನಿರ್ದಿಷ್ಟ ಆಯ್ಕೆ', 'Production cycle': 'ಉತ್ಪಾದನಾ ಚಕ್ರ', 'Space requirement': 'ಸ್ಥಳದ ಅವಶ್ಯಕತೆ', 'Climate compatibility': 'ಹವಾಮಾನ ಹೊಂದಾಣಿಕೆ', 'Target market': 'ಗುರಿ ಮಾರುಕಟ್ಟೆ', 'Execution Roadmap': 'ಕಾರ್ಯಗತಗೊಳಿಸುವ ಮಾರ್ಗಸೂಚಿ', 'Foundation & Setup': 'ಅಡಿಪಾಯ ಮತ್ತು ಸ್ಥಾಪನೆ', 'READY THE BUSINESS': 'ವ್ಯವಹಾರವನ್ನು ಸಿದ್ಧಪಡಿಸಿ', 'Procure & Pilot': 'ಖರೀದಿ ಮತ್ತು ಪೈಲಟ್', 'TEST BEFORE SCALE': 'ವಿಸ್ತರಿಸುವ ಮೊದಲು ಪರೀಕ್ಷಿಸಿ', 'Production, Market & Scale': 'ಉತ್ಪಾದನೆ, ಮಾರುಕಟ್ಟೆ ಮತ್ತು ವಿಸ್ತರಣೆ', 'TURN THE PILOT INTO A BUSINESS': 'ಪೈಲಟ್ ಅನ್ನು ವ್ಯವಹಾರವಾಗಿ ರೂಪಿಸಿ', 'Outcome:': 'ಫಲಿತಾಂಶ:', 'Scale rule': 'ವಿಸ್ತರಣೆ ನಿಯಮ', 'Route': 'ಮಾರ್ಗ', 'Practical use': 'ಪ್ರಾಯೋಗಿಕ ಬಳಕೆ', 'Pricing focus': 'ಬೆಲೆ ನಿಗದಿ ಗಮನ', 'Differentiation': 'ವಿಶಿಷ್ಟತೆ', 'Priority gaps': 'ಪ್ರಮುಖ ಕೊರತೆಗಳು', 'Gap': 'ಕೊರತೆ', 'Action': 'ಕ್ರಮ', 'Financial Benchmarks': 'ಹಣಕಾಸು ಮಾನದಂಡಗಳು', 'Benchmark': 'ಮಾನದಂಡ', 'Indicative value': 'ಅಂದಾಜು ಮೌಲ್ಯ', 'Interpretation': 'ವಿವರಣೆ', 'Minimum configured investment': 'ಕನಿಷ್ಠ ನಿಗದಿತ ಹೂಡಿಕೆ', 'Planned investment': 'ಯೋಜಿತ ಹೂಡಿಕೆ', 'Monthly operating cost': 'ಮಾಸಿಕ ಕಾರ್ಯಾಚರಣಾ ವೆಚ್ಚ', 'Annual benefit': 'ವಾರ್ಷಿಕ ಲಾಭ', 'Break-even': 'ಬ್ರೇಕ್-ಈವನ್', 'Feasibility indicator': 'ಕಾರ್ಯಸಾಧ್ಯತೆ ಸೂಚಕ', 'Value': 'ಮೌಲ್ಯ', 'Note': 'ಟಿಪ್ಪಣಿ', 'Scheme': 'ಯೋಜನೆ', 'What it supports': 'ಇದು ಯಾವುದಕ್ಕೆ ಬೆಂಬಲ ನೀಡುತ್ತದೆ', 'Financial assistance': 'ಹಣಕಾಸು ಸಹಾಯ', 'Eligibility': 'ಅರ್ಹತೆ', 'Key documents / conditions': 'ಮುಖ್ಯ ದಾಖಲೆಗಳು / ಷರತ್ತುಗಳು', 'Practical Decision Check': 'ಪ್ರಾಯೋಗಿಕ ನಿರ್ಧಾರ ಪರಿಶೀಲನೆ', 'Not estimated': 'ಅಂದಾಜು ಲಭ್ಯವಿಲ್ಲ', 'Not provided': 'ನೀಡಲಾಗಿಲ್ಲ', 'Not available': 'ಲಭ್ಯವಿಲ್ಲ', 'Indicative; verify locally': 'ಅಂದಾಜು; ಸ್ಥಳೀಯವಾಗಿ ಪರಿಶೀಲಿಸಿ', 'Current input / configured estimate': 'ಪ್ರಸ್ತುತ ಇನ್\u200cಪುಟ್ / ನಿಗದಿತ ಅಂದಾಜು', 'Indicative model estimate': 'ಅಂದಾಜು ಮಾದರಿ ಮೌಲ್ಯ', 'Adaptive score from available inputs': 'ಲಭ್ಯವಿರುವ ಇನ್\u200cಪುಟ್\u200cಗಳಿಂದ ಹೊಂದಿಕೊಳ್ಳುವ ಸ್ಕೋರ್', 'Indicative, scale-dependent': 'ಅಂದಾಜು, ಪ್ರಮಾಣದ ಮೇಲೆ ಅವಲಂಬಿತ', 'identified': 'ಗುರುತಿಸಲಾಗಿದೆ', 'item(s)': 'ಅಂಶ', 'Selection': 'ಆಯ್ಕೆ', 'Market & Advisory': 'ಮಾರುಕಟ್ಟೆ ಮತ್ತು ಸಲಹೆ', 'Risk Control': 'ಅಪಾಯ ನಿಯಂತ್ರಣ', 'Schemes': 'ಯೋಜನೆಗಳು'}}


# Complete Business Recommendation roadmap translations.
OUTPUT_TR.setdefault("Hindi", {}).update({
    "Make the site, resources, budget and compliance setup ready.": "स्थान, संसाधन, बजट और अनुपालन की तैयारी पूरी करें।",
    "Confirm land / workspace, water and access conditions.": "भूमि / कार्यस्थल, पानी और पहुंच की स्थिति की पुष्टि करें।",
    "Prepare a minimum investment plan and cash buffer.": "न्यूनतम निवेश योजना और नकद रिज़र्व तैयार करें।",
    "Complete required permits, registrations, testing or local checks.": "आवश्यक परमिट, पंजीकरण, परीक्षण या स्थानीय जांच पूरी करें।",
    "Site + resources + budget confirmed": "स्थान + संसाधन + बजट की पुष्टि",
    "Run a controlled pilot using the selected option and record real costs.": "चयनित विकल्प का नियंत्रित पायलट चलाएं और वास्तविक लागत दर्ज करें।",
    "Procure quality inputs / stock / equipment from traceable suppliers.": "विश्वसनीय और सत्यापित आपूर्तिकर्ताओं से गुणवत्तापूर्ण इनपुट / स्टॉक / उपकरण खरीदें।",
    "Start with a manageable pilot size and track labour, water and input use.": "प्रबंधनीय पायलट आकार से शुरुआत करें और श्रम, पानी तथा इनपुट के उपयोग को दर्ज करें।",
    "Record production, quality, demand and actual spending.": "उत्पादन, गुणवत्ता, मांग और वास्तविक खर्च दर्ज करें।",
    "Pilot data meets the planned operating thresholds": "पायलट डेटा नियोजित संचालन सीमाओं को पूरा करता है",
    "Move into repeat production, secure buyers and scale only where unit economics work.": "दोहराए जाने वाले उत्पादन में जाएं, खरीदार सुनिश्चित करें और केवल वहां विस्तार करें जहां प्रति-इकाई अर्थशास्त्र व्यवहार्य हो।",
    "Lock B2B + D2C sales channels and define pricing / pack strategy.": "B2B + D2C बिक्री चैनल तय करें और मूल्य निर्धारण / पैक रणनीति निर्धारित करें।",
    "Schedule production, grading, storage and transport.": "उत्पादन, ग्रेडिंग, भंडारण और परिवहन का समय निर्धारित करें।",
    "Review monthly cash flow and expand capacity in controlled steps.": "मासिक नकदी प्रवाह की समीक्षा करें और नियंत्रित चरणों में क्षमता बढ़ाएं।",
    "Repeat demand + workable unit economics + operational control": "दोहराई जाने वाली मांग + व्यवहार्य प्रति-इकाई अर्थशास्त्र + संचालन नियंत्रण",
    "Do not move straight from setup to full investment. Validate the pilot, actual operating cost and buyer response first.": "स्थापना से सीधे पूर्ण निवेश पर न जाएं। पहले पायलट, वास्तविक संचालन लागत और खरीदारों की प्रतिक्रिया को सत्यापित करें।",
    "Weeks 1–2": "सप्ताह 1–2",
    "Weeks 3–8": "सप्ताह 3–8",
    "After pilot validation": "पायलट सत्यापन के बाद",
    "Foundation & Setup": "अडिपाय और स्थापना",
    "Procure & Pilot": "खरीद और पायलट",
    "Production, Market & Scale": "उत्पादन, बाजार और विस्तार",
    "READY THE BUSINESS": "व्यवसाय को तैयार करें",
    "TEST BEFORE SCALE": "विस्तार से पहले परीक्षण करें",
    "TURN THE PILOT INTO A BUSINESS": "पायलट को व्यवसाय में बदलें",
})
OUTPUT_TR.setdefault("Kannada", {}).update({
    "Make the site, resources, budget and compliance setup ready.": "ಸ್ಥಳ, ಸಂಪನ್ಮೂಲಗಳು, ಬಜೆಟ್ ಮತ್ತು ಅನುಸರಣೆ ಸಿದ್ಧತೆಯನ್ನು ಪೂರ್ಣಗೊಳಿಸಿ.",
    "Confirm land / workspace, water and access conditions.": "ಭೂಮಿ / ಕೆಲಸದ ಸ್ಥಳ, ನೀರು ಮತ್ತು ಪ್ರವೇಶದ ಪರಿಸ್ಥಿತಿಗಳನ್ನು ಖಚಿತಪಡಿಸಿ.",
    "Prepare a minimum investment plan and cash buffer.": "ಕನಿಷ್ಠ ಹೂಡಿಕೆ ಯೋಜನೆ ಮತ್ತು ನಗದು ಮೀಸಲು ಸಿದ್ಧಪಡಿಸಿ.",
    "Complete required permits, registrations, testing or local checks.": "ಅಗತ್ಯ ಪರವಾನಗಿಗಳು, ನೋಂದಣಿಗಳು, ಪರೀಕ್ಷೆಗಳು ಅಥವಾ ಸ್ಥಳೀಯ ಪರಿಶೀಲನೆಗಳನ್ನು ಪೂರ್ಣಗೊಳಿಸಿ.",
    "Site + resources + budget confirmed": "ಸ್ಥಳ + ಸಂಪನ್ಮೂಲಗಳು + ಬಜೆಟ್ ದೃಢೀಕರಿಸಲಾಗಿದೆ",
    "Run a controlled pilot using the selected option and record real costs.": "ಆಯ್ಕೆ ಮಾಡಿದ ಆಯ್ಕೆಯನ್ನು ಬಳಸಿ ನಿಯಂತ್ರಿತ ಪೈಲಟ್ ನಡೆಸಿ ಮತ್ತು ನಿಜವಾದ ವೆಚ್ಚಗಳನ್ನು ದಾಖಲಿಸಿ.",
    "Procure quality inputs / stock / equipment from traceable suppliers.": "ವಿಶ್ವಾಸಾರ್ಹ ಮತ್ತು ಪರಿಶೀಲಿಸಬಹುದಾದ ಪೂರೈಕೆದಾರರಿಂದ ಗುಣಮಟ್ಟದ ಇನ್‌ಪುಟ್ / ಸ್ಟಾಕ್ / ಉಪಕರಣಗಳನ್ನು ಖರೀದಿಸಿ.",
    "Start with a manageable pilot size and track labour, water and input use.": "ನಿರ್ವಹಿಸಬಹುದಾದ ಪೈಲಟ್ ಗಾತ್ರದಿಂದ ಆರಂಭಿಸಿ ಮತ್ತು ಕಾರ್ಮಿಕ, ನೀರು ಹಾಗೂ ಇನ್‌ಪುಟ್ ಬಳಕೆಯನ್ನು ದಾಖಲಿಸಿ.",
    "Record production, quality, demand and actual spending.": "ಉತ್ಪಾದನೆ, ಗುಣಮಟ್ಟ, ಬೇಡಿಕೆ ಮತ್ತು ನಿಜವಾದ ಖರ್ಚನ್ನು ದಾಖಲಿಸಿ.",
    "Pilot data meets the planned operating thresholds": "ಪೈಲಟ್ ಡೇಟಾ ಯೋಜಿತ ಕಾರ್ಯಾಚರಣಾ ಮಿತಿಗಳನ್ನು ಪೂರೈಸುತ್ತದೆ",
    "Move into repeat production, secure buyers and scale only where unit economics work.": "ಪುನರಾವರ್ತಿತ ಉತ್ಪಾದನೆಗೆ ತೆರಳಿ, ಖರೀದಿದಾರರನ್ನು ಖಚಿತಪಡಿಸಿ ಮತ್ತು ಪ್ರತಿ ಘಟಕದ ಆರ್ಥಿಕತೆ ಕಾರ್ಯಸಾಧ್ಯವಾಗಿರುವಲ್ಲಿ ಮಾತ್ರ ವಿಸ್ತರಿಸಿ.",
    "Lock B2B + D2C sales channels and define pricing / pack strategy.": "B2B + D2C ಮಾರಾಟ ಚಾನೆಲ್‌ಗಳನ್ನು ನಿಗದಿಪಡಿಸಿ ಮತ್ತು ಬೆಲೆ / ಪ್ಯಾಕ್ ತಂತ್ರವನ್ನು ರೂಪಿಸಿ.",
    "Schedule production, grading, storage and transport.": "ಉತ್ಪಾದನೆ, ಗ್ರೇಡಿಂಗ್, ಸಂಗ್ರಹಣೆ ಮತ್ತು ಸಾರಿಗೆಯ ವೇಳಾಪಟ್ಟಿ ರೂಪಿಸಿ.",
    "Review monthly cash flow and expand capacity in controlled steps.": "ಮಾಸಿಕ ನಗದು ಹರಿವನ್ನು ಪರಿಶೀಲಿಸಿ ಮತ್ತು ನಿಯಂತ್ರಿತ ಹಂತಗಳಲ್ಲಿ ಸಾಮರ್ಥ್ಯವನ್ನು ಹೆಚ್ಚಿಸಿ.",
    "Repeat demand + workable unit economics + operational control": "ಪುನರಾವರ್ತಿತ ಬೇಡಿಕೆ + ಕಾರ್ಯಸಾಧ್ಯ ಪ್ರತಿ ಘಟಕದ ಆರ್ಥಿಕತೆ + ಕಾರ್ಯಾಚರಣಾ ನಿಯಂತ್ರಣ",
    "Do not move straight from setup to full investment. Validate the pilot, actual operating cost and buyer response first.": "ಸ್ಥಾಪನೆಯಿಂದ ನೇರವಾಗಿ ಪೂರ್ಣ ಹೂಡಿಕೆಗೆ ಹೋಗಬೇಡಿ. ಮೊದಲು ಪೈಲಟ್, ನಿಜವಾದ ಕಾರ್ಯಾಚರಣಾ ವೆಚ್ಚ ಮತ್ತು ಖರೀದಿದಾರರ ಪ್ರತಿಕ್ರಿಯೆಯನ್ನು ಪರಿಶೀಲಿಸಿ.",
    "Weeks 1–2": "ವಾರಗಳು 1–2",
    "Weeks 3–8": "ವಾರಗಳು 3–8",
    "After pilot validation": "ಪೈಲಟ್ ಪರಿಶೀಲನೆಯ ನಂತರ",
    "Foundation & Setup": "ಅಡಿಪಾಯ ಮತ್ತು ಸ್ಥಾಪನೆ",
    "Procure & Pilot": "ಖರೀದಿ ಮತ್ತು ಪೈಲಟ್",
    "Production, Market & Scale": "ಉತ್ಪಾದನೆ, ಮಾರುಕಟ್ಟೆ ಮತ್ತು ವಿಸ್ತರಣೆ",
    "READY THE BUSINESS": "ವ್ಯವಹಾರವನ್ನು ಸಿದ್ಧಪಡಿಸಿ",
    "TEST BEFORE SCALE": "ವಿಸ್ತರಿಸುವ ಮೊದಲು ಪರೀಕ್ಷಿಸಿ",
    "TURN THE PILOT INTO A BUSINESS": "ಪೈಲಟ್ ಅನ್ನು ವ್ಯವಹಾರವಾಗಿ ರೂಪಿಸಿ",
})


# Complete Business Recommendation output translations supplied for the
# Route, Risk Control, Financial Benchmarks, success criterion and Schemes.
OUTPUT_TR.setdefault("Hindi", {}).update({
    "Route": "मार्ग",
    "Practical use": "व्यावहारिक उपयोग",
    "Pricing focus": "मूल्य निर्धारण पर ध्यान",
    "B2B": "B2B",
    "D2C": "D2C",
    "Local institutional, wholesale or business buyers.": "स्थानीय संस्थागत, थोक या व्यावसायिक खरीदार।",
    "Compare net realized price after transport, handling and buyer deductions.": "परिवहन, हैंडलिंग और खरीदार की कटौतियों के बाद प्राप्त शुद्ध मूल्य की तुलना करें।",
    "Direct local households or end users where practical.": "जहां व्यावहारिक हो, स्थानीय परिवारों या अंतिम उपयोगकर्ताओं को सीधे बेचें।",
    "Test pack size, convenience, quality and repeat-purchase potential.": "पैक आकार, सुविधा, गुणवत्ता और दोबारा खरीद की संभावना का परीक्षण करें।",
    "Differentiation": "अलग पहचान",
    "Quality, grading, reliability, packaging or verified production practices where relevant.": "जहां प्रासंगिक हो, गुणवत्ता, ग्रेडिंग, विश्वसनीयता, पैकेजिंग या सत्यापित उत्पादन प्रक्रियाओं के आधार पर अलग पहचान बनाएं।",
    "Measure realized premium rather than assuming a premium.": "प्रीमियम मान लेने के बजाय वास्तविक रूप से प्राप्त प्रीमियम को मापें।",
    "Verify the main technical requirement and market channel before committing the full investment.": "पूर्ण निवेश करने से पहले मुख्य तकनीकी आवश्यकता और बाजार चैनल की पुष्टि करें।",
    "Use current local quotations for the startup and working-capital plan.": "स्टार्टअप और कार्यशील पूंजी योजना के लिए वर्तमान स्थानीय कोटेशन का उपयोग करें।",
    "Start with a manageable pilot and scale only after recording actual operating results.": "प्रबंधनीय पायलट से शुरुआत करें और वास्तविक संचालन परिणाम दर्ज करने के बाद ही विस्तार करें।",
    "Risk level": "अपरिपक्वता स्तर",
    "Impact": "प्रभाव",
    "Control / mitigation": "नियंत्रण / समाधान",
    "Market access risk": "बाजार पहुंच जोखिम",
    "Water availability risk": "पानी की उपलब्धता का जोखिम",
    "Biological crop risk": "जैविक फसल जोखिम",
    "Climate risk": "जलवायु जोखिम",
    "Crop price variation": "फसल मूल्य में बदलाव",
    "Input price variation": "इनपुट मूल्य में बदलाव",
    "Water availability": "पानी की उपलब्धता",
    "High": "उच्च",
    "Medium": "मध्यम",
    "Low": "कम",
    "High potential impact": "उच्च संभावित प्रभाव",
    "Identify at least two buyers before scaling, compare local prices weekly, and avoid expanding production until a selling channel is confirmed.": "विस्तार से पहले कम से कम दो खरीदारों की पहचान करें, स्थानीय कीमतों की साप्ताहिक तुलना करें और बिक्री चैनल की पुष्टि होने तक उत्पादन न बढ़ाएं।",
    "Secure a reliable source before scaling and maintain a contingency arrangement appropriate to the activity.": "विस्तार से पहले विश्वसनीय जल स्रोत सुनिश्चित करें और गतिविधि के अनुरूप वैकल्पिक व्यवस्था रखें।",
    "Use regular field scouting and preventive integrated management.": "नियमित खेत निरीक्षण और निवारक एकीकृत प्रबंधन अपनाएं।",
    "Use season-appropriate planning and a contingency response for extreme weather.": "मौसम के अनुसार योजना बनाएं और चरम मौसम के लिए वैकल्पिक प्रतिक्रिया तैयार रखें।",
    "Monitor this risk regularly and define a preventive response before scaling.": "इस जोखिम की नियमित निगरानी करें और विस्तार से पहले निवारक प्रतिक्रिया निर्धारित करें।",
    "Benchmark": "मानक",
    "Value": "मान",
    "Note": "टिप्पणी",
    "CAPEX": "पूंजीगत व्यय",
    "Validate with quotations.": "कोटेशन से सत्यापित करें।",
    "Feasibility": "व्यवहार्यता",
    "Adaptive rule-based score.": "अनुकूली नियम-आधारित स्कोर।",
    "Break-even": "ब्रेक-ईवन",
    "Not estimated": "अनुमानित नहीं",
    "Needs a configured financial model for this activity.": "इस गतिविधि के लिए कॉन्फ़िगर किया गया वित्तीय मॉडल आवश्यक है।",
    "Success criterion: Complete a pilot that records unit cost, production/service volume, actual selling price, loss/mortality where applicable, and customer acquisition cost before scaling.": "सफलता मानदंड: विस्तार से पहले इकाई लागत, उत्पादन/सेवा मात्रा, वास्तविक बिक्री मूल्य, जहां लागू हो वहां नुकसान/मृत्यु दर और ग्राहक प्राप्ति लागत दर्ज करने वाला पायलट पूरा करें।",
    "Success criterion": "सफलता मानदंड",
    "What it supports": "यह किसे सहायता करता है",
    "Financial assistance": "वित्तीय सहायता",
    "Eligibility": "पात्रता",
    "Key documents / conditions": "मुख्य दस्तावेज / शर्तें",
    "Kisan Credit Card (KCC)": "किसान क्रेडिट कार्ड (KCC)",
    "A formal agricultural credit mechanism for eligible crop and allied working-capital requirements.": "पात्र फसल और संबद्ध कार्यशील पूंजी आवश्यकताओं के लिए औपचारिक कृषि ऋण व्यवस्था।",
    "Provides access to institutional credit for eligible agricultural/allied needs, subject to lender and eligibility conditions.": "ऋणदाता और पात्रता शर्तों के अधीन, पात्र कृषि/संबद्ध आवश्यकताओं के लिए संस्थागत ऋण तक पहुंच प्रदान करता है।",
    "Farmer/borrower eligibility and sanctioned limits depend on the participating financial institution and applicable KCC rules.": "किसान/उधारकर्ता की पात्रता और स्वीकृत सीमा संबंधित वित्तीय संस्था तथा लागू KCC नियमों पर निर्भर करती है।",
    "KCC is credit, not a direct capital subsidy; repayment and lending conditions apply.": "KCC ऋण सुविधा है, प्रत्यक्ष पूंजी सब्सिडी नहीं; पुनर्भुगतान और ऋण शर्तें लागू होती हैं।",
    "Agriculture Infrastructure Fund (AIF)": "कृषि अवसंरचना निधि (AIF)",
    "A financing facility for eligible post-harvest management and agricultural infrastructure projects.": "पात्र फसल-कटाई के बाद प्रबंधन और कृषि अवसंरचना परियोजनाओं के लिए वित्तपोषण सुविधा।",
    "Official scheme material provides eligible borrowers with interest-support and credit-facilitation benefits subject to scheme conditions.": "आधिकारिक योजना सामग्री के अनुसार, योजना की शर्तों के अधीन पात्र उधारकर्ताओं को ब्याज सहायता और ऋण सुविधा लाभ मिलते हैं।",
    "Eligibility depends on the borrower category and the infrastructure asset/project being financed.": "पात्रता उधारकर्ता की श्रेणी और वित्तपोषित की जा रही अवसंरचना संपत्ति/परियोजना पर निर्भर करती है।",
    "The recommended project must fit an eligible infrastructure category and the current lending guidelines.": "अनुशंसित परियोजना को पात्र अवसंरचना श्रेणी और वर्तमान ऋण दिशानिर्देशों के अनुरूप होना चाहिए।",
})

OUTPUT_TR.setdefault("Kannada", {}).update({
    "Route": "ಮಾರ್ಗ",
    "Practical use": "ಪ್ರಾಯೋಗಿಕ ಬಳಕೆ",
    "Pricing focus": "ಬೆಲೆ ನಿಗದಿ ಗಮನ",
    "B2B": "B2B",
    "D2C": "D2C",
    "Local institutional, wholesale or business buyers.": "ಸ್ಥಳೀಯ ಸಂಸ್ಥೆಗಳು, ಸಗಟು ಖರೀದಿದಾರರು ಅಥವಾ ವ್ಯವಹಾರಿಕ ಖರೀದಿದಾರರು.",
    "Compare net realized price after transport, handling and buyer deductions.": "ಸಾರಿಗೆ, ನಿರ್ವಹಣೆ ಮತ್ತು ಖರೀದಿದಾರರ ಕಡಿತಗಳ ನಂತರ ದೊರೆಯುವ ನಿವ್ವಳ ಬೆಲೆಯನ್ನು ಹೋಲಿಸಿ.",
    "Direct local households or end users where practical.": "ಪ್ರಾಯೋಗಿಕವಾಗಿರುವಲ್ಲಿ ಸ್ಥಳೀಯ ಕುಟುಂಬಗಳು ಅಥವಾ ಅಂತಿಮ ಬಳಕೆದಾರರಿಗೆ ನೇರವಾಗಿ ಮಾರಾಟ ಮಾಡಿ.",
    "Test pack size, convenience, quality and repeat-purchase potential.": "ಪ್ಯಾಕ್ ಗಾತ್ರ, ಅನುಕೂಲತೆ, ಗುಣಮಟ್ಟ ಮತ್ತು ಮರುಖರೀದಿ ಸಾಧ್ಯತೆಯನ್ನು ಪರೀಕ್ಷಿಸಿ.",
    "Differentiation": "ವೈಶಿಷ್ಟ್ಯತೆ",
    "Quality, grading, reliability, packaging or verified production practices where relevant.": "ಅಗತ್ಯವಿರುವಲ್ಲಿ ಗುಣಮಟ್ಟ, ಗ್ರೇಡಿಂಗ್, ವಿಶ್ವಾಸಾರ್ಹತೆ, ಪ್ಯಾಕೇಜಿಂಗ್ ಅಥವಾ ಪರಿಶೀಲಿತ ಉತ್ಪಾದನಾ ವಿಧಾನಗಳ ಮೂಲಕ ವೈಶಿಷ್ಟ್ಯತೆ ರೂಪಿಸಿ.",
    "Measure realized premium rather than assuming a premium.": "ಪ್ರೀಮಿಯಂ ಇದೆ ಎಂದು ಊಹಿಸುವ ಬದಲು ನಿಜವಾಗಿ ದೊರೆತ ಪ್ರೀಮಿಯಂ ಅನ್ನು ಅಳೆಯಿರಿ.",
    "Verify the main technical requirement and market channel before committing the full investment.": "ಪೂರ್ಣ ಹೂಡಿಕೆಗೆ ಬದ್ಧರಾಗುವ ಮೊದಲು ಮುಖ್ಯ ತಾಂತ್ರಿಕ ಅವಶ್ಯಕತೆ ಮತ್ತು ಮಾರುಕಟ್ಟೆ ಚಾನೆಲ್ ಅನ್ನು ಪರಿಶೀಲಿಸಿ.",
    "Use current local quotations for the startup and working-capital plan.": "ಸ್ಟಾರ್ಟ್‌ಅಪ್ ಮತ್ತು ಕಾರ್ಯನಿರ್ವಹಣಾ ಬಂಡವಾಳ ಯೋಜನೆಗಾಗಿ ಪ್ರಸ್ತುತ ಸ್ಥಳೀಯ ಕೋಟೇಶನ್‌ಗಳನ್ನು ಬಳಸಿ.",
    "Start with a manageable pilot and scale only after recording actual operating results.": "ನಿರ್ವಹಿಸಬಹುದಾದ ಪೈಲಟ್‌ನಿಂದ ಆರಂಭಿಸಿ ಮತ್ತು ನಿಜವಾದ ಕಾರ್ಯಾಚರಣಾ ಫಲಿತಾಂಶಗಳನ್ನು ದಾಖಲಿಸಿದ ನಂತರ ಮಾತ್ರ ವಿಸ್ತರಿಸಿ.",
    "Risk level": "ಅಪಾಯ ಮಟ್ಟ",
    "Impact": "ಪರಿಣಾಮ",
    "Control / mitigation": "ನಿಯಂತ್ರಣ / ಪರಿಹಾರ",
    "Market access risk": "ಮಾರುಕಟ್ಟೆ ಪ್ರವೇಶ ಅಪಾಯ",
    "Water availability risk": "ನೀರಿನ ಲಭ್ಯತೆ ಅಪಾಯ",
    "Biological crop risk": "ಜೈವಿಕ ಬೆಳೆ ಅಪಾಯ",
    "Climate risk": "ಹವಾಮಾನ ಅಪಾಯ",
    "Crop price variation": "ಬೆಳೆ ಬೆಲೆ ಬದಲಾವಣೆ",
    "Input price variation": "ಇನ್‌ಪುಟ್ ಬೆಲೆ ಬದಲಾವಣೆ",
    "Water availability": "ನೀರಿನ ಲಭ್ಯತೆ",
    "High": "ಹೆಚ್ಚು",
    "Medium": "ಮಧ್ಯಮ",
    "Low": "ಕಡಿಮೆ",
    "High potential impact": "ಹೆಚ್ಚಿನ ಸಾಧ್ಯ ಪರಿಣಾಮ",
    "Identify at least two buyers before scaling, compare local prices weekly, and avoid expanding production until a selling channel is confirmed.": "ವಿಸ್ತರಿಸುವ ಮೊದಲು ಕನಿಷ್ಠ ಇಬ್ಬರು ಖರೀದಿದಾರರನ್ನು ಗುರುತಿಸಿ, ಸ್ಥಳೀಯ ಬೆಲೆಗಳನ್ನು ವಾರಕ್ಕೊಮ್ಮೆ ಹೋಲಿಸಿ ಮತ್ತು ಮಾರಾಟ ಚಾನೆಲ್ ದೃಢವಾಗುವವರೆಗೆ ಉತ್ಪಾದನೆಯನ್ನು ಹೆಚ್ಚಿಸಬೇಡಿ.",
    "Secure a reliable source before scaling and maintain a contingency arrangement appropriate to the activity.": "ವಿಸ್ತರಿಸುವ ಮೊದಲು ವಿಶ್ವಾಸಾರ್ಹ ನೀರಿನ ಮೂಲವನ್ನು ಖಚಿತಪಡಿಸಿ ಮತ್ತು ಚಟುವಟಿಕೆಗೆ ಸೂಕ್ತವಾದ ಪರ್ಯಾಯ ವ್ಯವಸ್ಥೆಯನ್ನು ಇಟ್ಟುಕೊಳ್ಳಿ.",
    "Use regular field scouting and preventive integrated management.": "ನಿಯಮಿತ ಹೊಲ ಪರಿಶೀಲನೆ ಮತ್ತು ತಡೆಗಟ್ಟುವ ಸಮಗ್ರ ನಿರ್ವಹಣೆಯನ್ನು ಬಳಸಿ.",
    "Use season-appropriate planning and a contingency response for extreme weather.": "ಋತುವಿಗೆ ಸೂಕ್ತವಾದ ಯೋಜನೆ ಮತ್ತು ತೀವ್ರ ಹವಾಮಾನಕ್ಕೆ ಪರ್ಯಾಯ ಪ್ರತಿಕ್ರಿಯೆಯನ್ನು ಬಳಸಿ.",
    "Monitor this risk regularly and define a preventive response before scaling.": "ಈ ಅಪಾಯವನ್ನು ನಿಯಮಿತವಾಗಿ ಮೇಲ್ವಿಚಾರಣೆ ಮಾಡಿ ಮತ್ತು ವಿಸ್ತರಿಸುವ ಮೊದಲು ತಡೆಗಟ್ಟುವ ಪ್ರತಿಕ್ರಿಯೆಯನ್ನು ನಿರ್ಧರಿಸಿ.",
    "Benchmark": "ಮಾನದಂಡ",
    "Value": "ಮೌಲ್ಯ",
    "Note": "ಟಿಪ್ಪಣಿ",
    "CAPEX": "ಬಂಡವಾಳ ವೆಚ್ಚ",
    "Validate with quotations.": "ಕೋಟೇಶನ್‌ಗಳಿಂದ ಪರಿಶೀಲಿಸಿ.",
    "Feasibility": "ಕಾರ್ಯಸಾಧ್ಯತೆ",
    "Adaptive rule-based score.": "ಹೊಂದಿಕೊಳ್ಳುವ ನಿಯಮ-ಆಧಾರಿತ ಸ್ಕೋರ್.",
    "Break-even": "ಬ್ರೇಕ್-ಈವನ್",
    "Not estimated": "ಅಂದಾಜಿಸಲಾಗಿಲ್ಲ",
    "Needs a configured financial model for this activity.": "ಈ ಚಟುವಟಿಕೆಗೆ ಕಾನ್ಫಿಗರ್ ಮಾಡಲಾದ ಹಣಕಾಸು ಮಾದರಿ ಅಗತ್ಯವಿದೆ.",
    "Success criterion: Complete a pilot that records unit cost, production/service volume, actual selling price, loss/mortality where applicable, and customer acquisition cost before scaling.": "ಯಶಸ್ಸಿನ ಮಾನದಂಡ: ವಿಸ್ತರಿಸುವ ಮೊದಲು ಘಟಕ ವೆಚ್ಚ, ಉತ್ಪಾದನೆ/ಸೇವಾ ಪ್ರಮಾಣ, ನಿಜವಾದ ಮಾರಾಟ ಬೆಲೆ, ಅನ್ವಯಿಸಿದಲ್ಲಿ ನಷ್ಟ/ಸಾವು ಪ್ರಮಾಣ ಮತ್ತು ಗ್ರಾಹಕ ಗಳಿಕೆ ವೆಚ್ಚವನ್ನು ದಾಖಲಿಸುವ ಪೈಲಟ್ ಪೂರ್ಣಗೊಳಿಸಿ.",
    "Success criterion": "ಯಶಸ್ಸಿನ ಮಾನದಂಡ",
    "What it supports": "ಇದು ಯಾವುದಕ್ಕೆ ಸಹಾಯ ಮಾಡುತ್ತದೆ",
    "Financial assistance": "ಹಣಕಾಸಿನ ನೆರವು",
    "Eligibility": "ಅರ್ಹತೆ",
    "Key documents / conditions": "ಮುಖ್ಯ ದಾಖಲೆಗಳು / ಷರತ್ತುಗಳು",
    "Kisan Credit Card (KCC)": "ಕಿಸಾನ್ ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್ (KCC)",
    "A formal agricultural credit mechanism for eligible crop and allied working-capital requirements.": "ಅರ್ಹ ಬೆಳೆ ಮತ್ತು ಸಂಬಂಧಿತ ಕಾರ್ಯನಿರ್ವಹಣಾ ಬಂಡವಾಳ ಅಗತ್ಯಗಳಿಗಾಗಿ ಅಧಿಕೃತ ಕೃಷಿ ಸಾಲ ವ್ಯವಸ್ಥೆ.",
    "Provides access to institutional credit for eligible agricultural/allied needs, subject to lender and eligibility conditions.": "ಸಾಲದಾತ ಮತ್ತು ಅರ್ಹತಾ ಷರತ್ತುಗಳಿಗೆ ಒಳಪಟ್ಟು, ಅರ್ಹ ಕೃಷಿ/ಸಂಬಂಧಿತ ಅಗತ್ಯಗಳಿಗೆ ಸಂಸ್ಥೆಯ ಸಾಲ ಸೌಲಭ್ಯವನ್ನು ಒದಗಿಸುತ್ತದೆ.",
    "Farmer/borrower eligibility and sanctioned limits depend on the participating financial institution and applicable KCC rules.": "ರೈತ/ಸಾಲಗಾರರ ಅರ್ಹತೆ ಮತ್ತು ಮಂಜೂರಾದ ಮಿತಿಗಳು ಭಾಗವಹಿಸುವ ಹಣಕಾಸು ಸಂಸ್ಥೆ ಹಾಗೂ ಅನ್ವಯಿಸುವ KCC ನಿಯಮಗಳ ಮೇಲೆ ಅವಲಂಬಿತವಾಗಿವೆ.",
    "KCC is credit, not a direct capital subsidy; repayment and lending conditions apply.": "KCC ಸಾಲ ಸೌಲಭ್ಯವಾಗಿದ್ದು, ನೇರ ಬಂಡವಾಳ ಸಬ್ಸಿಡಿ ಅಲ್ಲ; ಮರುಪಾವತಿ ಮತ್ತು ಸಾಲದ ಷರತ್ತುಗಳು ಅನ್ವಯಿಸುತ್ತವೆ.",
    "Agriculture Infrastructure Fund (AIF)": "ಕೃಷಿ ಮೂಲಸೌಕರ್ಯ ನಿಧಿ (AIF)",
    "A financing facility for eligible post-harvest management and agricultural infrastructure projects.": "ಅರ್ಹ ಕೊಯ್ಲಿನ ನಂತರದ ನಿರ್ವಹಣೆ ಮತ್ತು ಕೃಷಿ ಮೂಲಸೌಕರ್ಯ ಯೋಜನೆಗಳಿಗೆ ಹಣಕಾಸು ಸೌಲಭ್ಯ.",
    "Official scheme material provides eligible borrowers with interest-support and credit-facilitation benefits subject to scheme conditions.": "ಯೋಜನೆಯ ಷರತ್ತುಗಳಿಗೆ ಒಳಪಟ್ಟು ಅರ್ಹ ಸಾಲಗಾರರಿಗೆ ಬಡ್ಡಿ ನೆರವು ಮತ್ತು ಸಾಲ ಸೌಲಭ್ಯ ಪ್ರಯೋಜನಗಳನ್ನು ಅಧಿಕೃತ ಯೋಜನಾ ಮಾಹಿತಿಯು ಒದಗಿಸುತ್ತದೆ.",
    "Eligibility depends on the borrower category and the infrastructure asset/project being financed.": "ಅರ್ಹತೆಯು ಸಾಲಗಾರರ ವರ್ಗ ಮತ್ತು ಹಣಕಾಸು ಒದಗಿಸಲಾಗುತ್ತಿರುವ ಮೂಲಸೌಕರ್ಯ ಆಸ್ತಿ/ಯೋಜನೆಯ ಮೇಲೆ ಅವಲಂಬಿತವಾಗಿದೆ.",
    "The recommended project must fit an eligible infrastructure category and the current lending guidelines.": "ಶಿಫಾರಸು ಮಾಡಲಾದ ಯೋಜನೆಯು ಅರ್ಹ ಮೂಲಸೌಕರ್ಯ ವರ್ಗ ಮತ್ತು ಪ್ರಸ್ತುತ ಸಾಲ ಮಾರ್ಗಸೂಚಿಗಳಿಗೆ ಹೊಂದಿಕೆಯಾಗಿರಬೇಕು.",
})


# Kannada translations for the complete Business Recommendation content.
# These are exact UI/output strings, so the English version remains unchanged
# when English is selected.
PASTED_KANNADA_OUTPUT = {
    "Route": "ಮಾರ್ಗ",
    "Practical use": "ಪ್ರಾಯೋಗಿಕ ಬಳಕೆ",
    "Pricing focus": "ಬೆಲೆ ನಿಗದಿ ಗಮನ",
    "Local institutional, wholesale or business buyers.": "ಸ್ಥಳೀಯ ಸಂಸ್ಥೆಗಳು, ಸಗಟು ಅಥವಾ ವ್ಯವಹಾರಿಕ ಖರೀದಿದಾರರು.",
    "Compare net realized price after transport, handling and buyer deductions.": "ಸಾರಿಗೆ, ನಿರ್ವಹಣೆ ಮತ್ತು ಖರೀದಿದಾರರ ಕಡಿತಗಳ ನಂತರ ದೊರೆಯುವ ನಿವ್ವಳ ಬೆಲೆಯನ್ನು ಹೋಲಿಸಿ.",
    "Direct local households or end users where practical.": "ಪ್ರಾಯೋಗಿಕವಾಗಿರುವಲ್ಲಿ ಸ್ಥಳೀಯ ಕುಟುಂಬಗಳು ಅಥವಾ ಅಂತಿಮ ಬಳಕೆದಾರರಿಗೆ ನೇರವಾಗಿ ಮಾರಾಟ ಮಾಡಿ.",
    "Test pack size, convenience, quality and repeat-purchase potential.": "ಪ್ಯಾಕ್ ಗಾತ್ರ, ಅನುಕೂಲತೆ, ಗುಣಮಟ್ಟ ಮತ್ತು ಮರುಖರೀದಿ ಸಾಧ್ಯತೆಯನ್ನು ಪರೀಕ್ಷಿಸಿ.",
    "Quality, grading, reliability, packaging or verified production practices where relevant.": "ಅಗತ್ಯವಿರುವಲ್ಲಿ ಗುಣಮಟ್ಟ, ಗ್ರೇಡಿಂಗ್, ವಿಶ್ವಾಸಾರ್ಹತೆ, ಪ್ಯಾಕೇಜಿಂಗ್ ಅಥವಾ ಪರಿಶೀಲಿತ ಉತ್ಪಾದನಾ ವಿಧಾನಗಳ ಮೂಲಕ ವೈಶಿಷ್ಟ್ಯತೆ ರೂಪಿಸಿ.",
    "Measure realized premium rather than assuming a premium.": "ಪ್ರೀಮಿಯಂ ಇದೆ ಎಂದು ಊಹಿಸುವ ಬದಲು ನಿಜವಾಗಿ ದೊರೆತ ಪ್ರೀಮಿಯಂ ಅನ್ನು ಅಳೆಯಿರಿ.",
    "Verify the main technical requirement and market channel before committing the full investment.": "ಪೂರ್ಣ ಹೂಡಿಕೆಗೆ ಬದ್ಧರಾಗುವ ಮೊದಲು ಮುಖ್ಯ ತಾಂತ್ರಿಕ ಅವಶ್ಯಕತೆ ಮತ್ತು ಮಾರುಕಟ್ಟೆ ಚಾನೆಲ್ ಅನ್ನು ಪರಿಶೀಲಿಸಿ.",
    "Use current local quotations for the startup and working-capital plan.": "ಸ್ಟಾರ್ಟ್‌ಅಪ್ ಮತ್ತು ಕಾರ್ಯನಿರ್ವಹಣಾ ಬಂಡವಾಳ ಯೋಜನೆಗಾಗಿ ಪ್ರಸ್ತುತ ಸ್ಥಳೀಯ ಕೋಟೇಶನ್‌ಗಳನ್ನು ಬಳಸಿ.",
    "Start with a manageable pilot and scale only after recording actual operating results.": "ನಿರ್ವಹಿಸಬಹುದಾದ ಪೈಲಟ್‌ನಿಂದ ಆರಂಭಿಸಿ ಮತ್ತು ನಿಜವಾದ ಕಾರ್ಯಾಚರಣಾ ಫಲಿತಾಂಶಗಳನ್ನು ದಾಖಲಿಸಿದ ನಂತರ ಮಾತ್ರ ವಿಸ್ತರಿಸಿ.",

    "Risk level": "ಅಪಾಯ ಮಟ್ಟ",
    "Impact": "ಪರಿಣಾಮ",
    "Control / mitigation": "ನಿಯಂತ್ರಣ / ಪರಿಹಾರ",
    "Market access risk": "ಮಾರುಕಟ್ಟೆ ಪ್ರವೇಶ ಅಪಾಯ",
    "Water availability risk": "ನೀರಿನ ಲಭ್ಯತೆ ಅಪಾಯ",
    "Biological crop risk": "ಜೈವಿಕ ಬೆಳೆ ಅಪಾಯ",
    "Climate risk": "ಹವಾಮಾನ ಅಪಾಯ",
    "Crop price variation": "ಬೆಳೆ ಬೆಲೆ ಬದಲಾವಣೆ",
    "Input price variation": "ಇನ್‌ಪುಟ್ ಬೆಲೆ ಬದಲಾವಣೆ",
    "Water availability": "ನೀರಿನ ಲಭ್ಯತೆ",
    "High": "ಹೆಚ್ಚು",
    "Medium": "ಮಧ್ಯಮ",
    "Low": "ಕಡಿಮೆ",
    "High potential impact": "ಹೆಚ್ಚಿನ ಸಾಧ್ಯ ಪರಿಣಾಮ",
    "—": "—",
    "Identify at least two buyers before scaling, compare local prices weekly, and avoid expanding production until a selling channel is confirmed.": "ವಿಸ್ತರಿಸುವ ಮೊದಲು ಕನಿಷ್ಠ ಇಬ್ಬರು ಖರೀದಿದಾರರನ್ನು ಗುರುತಿಸಿ, ಸ್ಥಳೀಯ ಬೆಲೆಗಳನ್ನು ವಾರಕ್ಕೊಮ್ಮೆ ಹೋಲಿಸಿ ಮತ್ತು ಮಾರಾಟ ಚಾನೆಲ್ ದೃಢವಾಗುವವರೆಗೆ ಉತ್ಪಾದನೆಯನ್ನು ಹೆಚ್ಚಿಸಬೇಡಿ.",
    "Secure a reliable source before scaling and maintain a contingency arrangement appropriate to the activity.": "ವಿಸ್ತರಿಸುವ ಮೊದಲು ವಿಶ್ವಾಸಾರ್ಹ ನೀರಿನ ಮೂಲವನ್ನು ಖಚಿತಪಡಿಸಿ ಮತ್ತು ಚಟುವಟಿಕೆಗೆ ಸೂಕ್ತವಾದ ಪರ್ಯಾಯ ವ್ಯವಸ್ಥೆಯನ್ನು ಇಟ್ಟುಕೊಳ್ಳಿ.",
    "Use regular field scouting and preventive integrated management.": "ನಿಯಮಿತ ಹೊಲ ಪರಿಶೀಲನೆ ಮತ್ತು ತಡೆಗಟ್ಟುವ ಸಮಗ್ರ ನಿರ್ವಹಣೆಯನ್ನು ಬಳಸಿ.",
    "Use season-appropriate planning and a contingency response for extreme weather.": "ಋತುವಿಗೆ ಸೂಕ್ತವಾದ ಯೋಜನೆ ಮತ್ತು ತೀವ್ರ ಹವಾಮಾನಕ್ಕೆ ಪರ್ಯಾಯ ಪ್ರತಿಕ್ರಿಯೆಯನ್ನು ಬಳಸಿ.",
    "Monitor this risk regularly and define a preventive response before scaling.": "ಈ ಅಪಾಯವನ್ನು ನಿಯಮಿತವಾಗಿ ಮೇಲ್ವಿಚಾರಣೆ ಮಾಡಿ ಮತ್ತು ವಿಸ್ತರಿಸುವ ಮೊದಲು ತಡೆಗಟ್ಟುವ ಪ್ರತಿಕ್ರಿಯೆಯನ್ನು ನಿರ್ಧರಿಸಿ.",

    "Benchmark": "ಮಾನದಂಡ",
    "Value": "ಮೌಲ್ಯ",
    "Note": "ಟಿಪ್ಪಣಿ",
    "CAPEX": "ಬಂಡವಾಳ ವೆಚ್ಚ",
    "Validate with quotations.": "ಕೋಟೇಶನ್‌ಗಳಿಂದ ಪರಿಶೀಲಿಸಿ.",
    "Feasibility": "ಕಾರ್ಯಸಾಧ್ಯತೆ",
    "Adaptive rule-based score.": "ಹೊಂದಿಕೊಳ್ಳುವ ನಿಯಮ-ಆಧಾರಿತ ಸ್ಕೋರ್.",
    "Break-even": "ಬ್ರೇಕ್-ಈವನ್",
    "Not estimated": "ಅಂದಾಜಿಸಲಾಗಿಲ್ಲ",
    "Needs a configured financial model for this activity.": "ಈ ಚಟುವಟಿಕೆಗೆ ಕಾನ್ಫಿಗರ್ ಮಾಡಲಾದ ಹಣಕಾಸು ಮಾದರಿ ಅಗತ್ಯವಿದೆ.",

    "Success criterion": "ಯಶಸ್ಸಿನ ಮಾನದಂಡ",
    "Success criterion: Complete a pilot that records unit cost, production/service volume, actual selling price, loss/mortality where applicable, and customer acquisition cost before scaling.": "ಯಶಸ್ಸಿನ ಮಾನದಂಡ: ವಿಸ್ತರಿಸುವ ಮೊದಲು ಘಟಕ ವೆಚ್ಚ, ಉತ್ಪಾದನೆ/ಸೇವಾ ಪ್ರಮಾಣ, ನಿಜವಾದ ಮಾರಾಟ ಬೆಲೆ, ಅನ್ವಯಿಸಿದಲ್ಲಿ ನಷ್ಟ/ಸಾವು ಪ್ರಮಾಣ ಮತ್ತು ಗ್ರಾಹಕ ಗಳಿಕೆ ವೆಚ್ಚವನ್ನು ದಾಖಲಿಸುವ ಪೈಲಟ್ ಪೂರ್ಣಗೊಳಿಸಿ.",

    "Scheme": "ಯೋಜನೆ",
    "What it supports": "ಇದು ಯಾವುದಕ್ಕೆ ಸಹಾಯ ಮಾಡುತ್ತದೆ",
    "Financial assistance": "ಹಣಕಾಸಿನ ನೆರವು",
    "Eligibility": "ಅರ್ಹತೆ",
    "Key documents / conditions": "ಮುಖ್ಯ ದಾಖಲೆಗಳು / ಷರತ್ತುಗಳು",
    "Kisan Credit Card (KCC)": "ಕಿಸಾನ್ ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್ (KCC)",
    "A formal agricultural credit mechanism for eligible crop and allied working-capital requirements.": "ಅರ್ಹ ಬೆಳೆ ಮತ್ತು ಸಂಬಂಧಿತ ಕಾರ್ಯನಿರ್ವಹಣಾ ಬಂಡವಾಳ ಅಗತ್ಯಗಳಿಗಾಗಿ ಅಧಿಕೃತ ಕೃಷಿ ಸಾಲ ವ್ಯವಸ್ಥೆ.",
    "Provides access to institutional credit for eligible agricultural/allied needs, subject to lender and eligibility conditions.": "ಸಾಲದಾತ ಮತ್ತು ಅರ್ಹತಾ ಷರತ್ತುಗಳಿಗೆ ಒಳಪಟ್ಟು, ಅರ್ಹ ಕೃಷಿ/ಸಂಬಂಧಿತ ಅಗತ್ಯಗಳಿಗೆ ಸಂಸ್ಥೆಯ ಸಾಲ ಸೌಲಭ್ಯವನ್ನು ಒದಗಿಸುತ್ತದೆ.",
    "Farmer/borrower eligibility and sanctioned limits depend on the participating financial institution and applicable KCC rules.": "ರೈತ/ಸಾಲಗಾರರ ಅರ್ಹತೆ ಮತ್ತು ಮಂಜೂರಾದ ಮಿತಿಗಳು ಭಾಗವಹಿಸುವ ಹಣಕಾಸು ಸಂಸ್ಥೆ ಹಾಗೂ ಅನ್ವಯಿಸುವ KCC ನಿಯಮಗಳ ಮೇಲೆ ಅವಲಂಬಿತವಾಗಿವೆ.",
    "KCC is credit, not a direct capital subsidy; repayment and lending conditions apply.": "KCC ಸಾಲ ಸೌಲಭ್ಯವಾಗಿದ್ದು, ನೇರ ಬಂಡವಾಳ ಸಬ್ಸಿಡಿ ಅಲ್ಲ; ಮರುಪಾವತಿ ಮತ್ತು ಸಾಲದ ಷರತ್ತುಗಳು ಅನ್ವಯಿಸುತ್ತವೆ.",
    "Agriculture Infrastructure Fund (AIF)": "ಕೃಷಿ ಮೂಲಸೌಕರ್ಯ ನಿಧಿ (AIF)",
    "A financing facility for eligible post-harvest management and agricultural infrastructure projects.": "ಅರ್ಹ ಕೊಯ್ಲಿನ ನಂತರದ ನಿರ್ವಹಣೆ ಮತ್ತು ಕೃಷಿ ಮೂಲಸೌಕರ್ಯ ಯೋಜನೆಗಳಿಗೆ ಹಣಕಾಸು ಸೌಲಭ್ಯ.",
    "Official scheme material provides eligible borrowers with interest-support and credit-facilitation benefits subject to scheme conditions.": "ಯೋಜನೆಯ ಷರತ್ತುಗಳಿಗೆ ಒಳಪಟ್ಟು ಅರ್ಹ ಸಾಲಗಾರರಿಗೆ ಬಡ್ಡಿ ನೆರವು ಮತ್ತು ಸಾಲ ಸೌಲಭ್ಯ ಪ್ರಯೋಜನಗಳನ್ನು ಅಧಿಕೃತ ಯೋಜನಾ ಮಾಹಿತಿಯು ಒದಗಿಸುತ್ತದೆ.",
    "Eligibility depends on the borrower category and the infrastructure asset/project being financed.": "ಅರ್ಹತೆಯು ಸಾಲಗಾರರ ವರ್ಗ ಮತ್ತು ಹಣಕಾಸು ಒದಗಿಸಲಾಗುತ್ತಿರುವ ಮೂಲಸೌಕರ್ಯ ಆಸ್ತಿ/ಯೋಜನೆಯ ಮೇಲೆ ಅವಲಂಬಿತವಾಗಿದೆ.",
    "The recommended project must fit an eligible infrastructure category and the current lending guidelines.": "ಶಿಫಾರಸು ಮಾಡಲಾದ ಯೋಜನೆಯು ಅರ್ಹ ಮೂಲಸೌಕರ್ಯ ವರ್ಗ ಮತ್ತು ಪ್ರಸ್ತುತ ಸಾಲ ಮಾರ್ಗಸೂಚಿಗಳಿಗೆ ಹೊಂದಿಕೆಯಾಗಿರಬೇಕು.",

    # Roadmap
    "Make the site, resources, budget and compliance setup ready.": "ಸ್ಥಳ, ಸಂಪನ್ಮೂಲಗಳು, ಬಜೆಟ್ ಮತ್ತು ಅನುಸರಣೆ ಸಿದ್ಧತೆಯನ್ನು ಪೂರ್ಣಗೊಳಿಸಿ.",
    "Confirm land / workspace, water and access conditions.": "ಭೂಮಿ / ಕೆಲಸದ ಸ್ಥಳ, ನೀರು ಮತ್ತು ಪ್ರವೇಶದ ಪರಿಸ್ಥಿತಿಗಳನ್ನು ಖಚಿತಪಡಿಸಿ.",
    "Prepare a minimum investment plan and cash buffer.": "ಕನಿಷ್ಠ ಹೂಡಿಕೆ ಯೋಜನೆ ಮತ್ತು ನಗದು ಮೀಸಲು ಸಿದ್ಧಪಡಿಸಿ.",
    "Complete required permits, registrations, testing or local checks.": "ಅಗತ್ಯ ಪರವಾನಗಿಗಳು, ನೋಂದಣಿಗಳು, ಪರೀಕ್ಷೆಗಳು ಅಥವಾ ಸ್ಥಳೀಯ ಪರಿಶೀಲನೆಗಳನ್ನು ಪೂರ್ಣಗೊಳಿಸಿ.",
    "Site + resources + budget confirmed": "ಸ್ಥಳ + ಸಂಪನ್ಮೂಲಗಳು + ಬಜೆಟ್ ದೃಢೀಕರಿಸಲಾಗಿದೆ",
    "Run a controlled pilot using the selected option and record real costs.": "ಆಯ್ಕೆ ಮಾಡಿದ ಆಯ್ಕೆಯನ್ನು ಬಳಸಿ ನಿಯಂತ್ರಿತ ಪೈಲಟ್ ನಡೆಸಿ ಮತ್ತು ನಿಜವಾದ ವೆಚ್ಚಗಳನ್ನು ದಾಖಲಿಸಿ.",
    "Procure quality inputs / stock / equipment from traceable suppliers.": "ವಿಶ್ವಾಸಾರ್ಹ ಮತ್ತು ಪರಿಶೀಲಿಸಬಹುದಾದ ಪೂರೈಕೆದಾರರಿಂದ ಗುಣಮಟ್ಟದ ಇನ್‌ಪುಟ್ / ಸ್ಟಾಕ್ / ಉಪಕರಣಗಳನ್ನು ಖರೀದಿಸಿ.",
    "Start with a manageable pilot size and track labour, water and input use.": "ನಿರ್ವಹಿಸಬಹುದಾದ ಪೈಲಟ್ ಗಾತ್ರದಿಂದ ಆರಂಭಿಸಿ ಮತ್ತು ಕಾರ್ಮಿಕ, ನೀರು ಹಾಗೂ ಇನ್‌ಪುಟ್ ಬಳಕೆಯನ್ನು ದಾಖಲಿಸಿ.",
    "Record production, quality, demand and actual spending.": "ಉತ್ಪಾದನೆ, ಗುಣಮಟ್ಟ, ಬೇಡಿಕೆ ಮತ್ತು ನಿಜವಾದ ಖರ್ಚನ್ನು ದಾಖಲಿಸಿ.",
    "Pilot data meets the planned operating thresholds": "ಪೈಲಟ್ ಡೇಟಾ ಯೋಜಿತ ಕಾರ್ಯಾಚರಣಾ ಮಿತಿಗಳನ್ನು ಪೂರೈಸುತ್ತದೆ",
    "Move into repeat production, secure buyers and scale only where unit economics work.": "ಪುನರಾವರ್ತಿತ ಉತ್ಪಾದನೆಗೆ ತೆರಳಿ, ಖರೀದಿದಾರರನ್ನು ಖಚಿತಪಡಿಸಿ ಮತ್ತು ಪ್ರತಿ ಘಟಕದ ಆರ್ಥಿಕತೆ ಕಾರ್ಯಸಾಧ್ಯವಾಗಿರುವಲ್ಲಿ ಮಾತ್ರ ವಿಸ್ತರಿಸಿ.",
    "Lock B2B + D2C sales channels and define pricing / pack strategy.": "B2B + D2C ಮಾರಾಟ ಚಾನೆಲ್‌ಗಳನ್ನು ನಿಗದಿಪಡಿಸಿ ಮತ್ತು ಬೆಲೆ / ಪ್ಯಾಕ್ ತಂತ್ರವನ್ನು ರೂಪಿಸಿ.",
    "Schedule production, grading, storage and transport.": "ಉತ್ಪಾದನೆ, ಗ್ರೇಡಿಂಗ್, ಸಂಗ್ರಹಣೆ ಮತ್ತು ಸಾರಿಗೆಯ ವೇಳಾಪಟ್ಟಿ ರೂಪಿಸಿ.",
    "Review monthly cash flow and expand capacity in controlled steps.": "ಮಾಸಿಕ ನಗದು ಹರಿವನ್ನು ಪರಿಶೀಲಿಸಿ ಮತ್ತು ನಿಯಂತ್ರಿತ ಹಂತಗಳಲ್ಲಿ ಸಾಮರ್ಥ್ಯವನ್ನು ಹೆಚ್ಚಿಸಿ.",
    "Repeat demand + workable unit economics + operational control": "ಪುನರಾವರ್ತಿತ ಬೇಡಿಕೆ + ಕಾರ್ಯಸಾಧ್ಯ ಪ್ರತಿ ಘಟಕದ ಆರ್ಥಿಕತೆ + ಕಾರ್ಯಾಚರಣಾ ನಿಯಂತ್ರಣ",
    "Do not move straight from setup to full investment. Validate the pilot, actual operating cost and buyer response first.": "ಸ್ಥಾಪನೆಯಿಂದ ನೇರವಾಗಿ ಪೂರ್ಣ ಹೂಡಿಕೆಗೆ ಹೋಗಬೇಡಿ. ಮೊದಲು ಪೈಲಟ್, ನಿಜವಾದ ಕಾರ್ಯಾಚರಣಾ ವೆಚ್ಚ ಮತ್ತು ಖರೀದಿದಾರರ ಪ್ರತಿಕ್ರಿಯೆಯನ್ನು ಪರಿಶೀಲಿಸಿ.",
    "Weeks 1–2": "ವಾರಗಳು 1–2",
    "Weeks 3–8": "ವಾರಗಳು 3–8",
    "After pilot validation": "ಪೈಲಟ್ ಪರಿಶೀಲನೆಯ ನಂತರ",
}

def safe_float(value, default=0.0):
    """Safely convert user/config values to float."""
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def translate_output_recursive(value):
    """Translate Business Recommendation output values recursively."""
    if isinstance(value, dict):
        return {k: translate_output_recursive(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        translated = [translate_output_recursive(v) for v in value]
        return type(value)(translated) if isinstance(value, tuple) else translated
    if isinstance(value, str):
        return tr_any(value)
    return value

def _current_language():
    """Return the active UI language safely at every point in the app lifecycle."""
    try:
        return _gs_lang()
    except Exception:
        try:
            return st.session_state.get("language", "English")
        except Exception:
            return "English"

def tr_any(value, **kwargs):
    text = str(value)
    lang = _current_language()
    # 1. Exact translation from all existing dictionaries.
    translated = TEXT.get(lang, {}).get(text, None)
    if translated is None:
        translated = UI_WORD_TR.get(lang, {}).get(text, None)
    if translated is None:
        translated = ENV_UI_TR.get(lang, {}).get(text, None)
    if translated is None:
        translated = OUTPUT_TR.get(lang, {}).get(text, None)
    if translated is None:
        # 2. Crop/category/trend values.
        translated = DATA_TR.get(lang, {}).get(text, None)
    if translated is None:
        translated = text
    return translated.format(**kwargs) if kwargs else translated

# Display translations for the crop/category/trend content.

# Display names for business domains, activities, common input values and risk/output terms.
BUSINESS_DISPLAY_TR = {
    "Hindi": {
        "Agriculture":"कृषि", "Livestock":"पशुपालन", "Aquaculture":"मत्स्य पालन", "Food Processing":"खाद्य प्रसंस्करण", "Services":"सेवाएँ", "Retail":"खुदरा",
        "Crop Cultivation":"फसल खेती", "Vegetable Cultivation":"सब्ज़ी खेती", "Fruit Cultivation":"फल खेती", "Spice Cultivation":"मसाला खेती", "Floriculture":"फूलों की खेती",
        "Poultry Farming":"पोल्ट्री फार्मिंग", "Dairy Farming":"डेयरी फार्मिंग", "Goat Farming":"बकरी पालन", "Sheep Farming":"भेड़ पालन", "Fish Farming":"मछली पालन",
        "Kharif":"खरीफ", "Rabi":"रबी", "Summer":"ग्रीष्म", "None":"नहीं", "Low":"कम", "Medium":"मध्यम", "High":"अधिक", "Poor":"कमज़ोर", "Moderate":"मध्यम", "Good":"अच्छा", "No":"नहीं", "Partial":"आंशिक", "Yes":"हाँ", "Shared":"साझा", "Available":"उपलब्ध", "Reliable":"विश्वसनीय", "Rain-fed":"वर्षा आधारित", "Limited":"सीमित", "Beginner":"शुरुआती", "Some experience":"कुछ अनुभव", "Experienced":"अनुभवी", "Within 3 months":"3 महीने के भीतर", "3–6 months":"3–6 महीने", "6–12 months":"6–12 महीने", "12+ months":"12+ महीने",
        "Weather variability":"मौसम में बदलाव", "Water availability":"पानी की उपलब्धता", "Input-price changes":"इनपुट कीमतों में बदलाव", "Crop-price changes":"फसल कीमतों में बदलाव", "Pest/disease pressure":"कीट/रोग का दबाव", "Price fluctuations":"कीमत में उतार-चढ़ाव", "Water stress":"पानी का तनाव", "Market-price changes":"बाज़ार कीमतों में बदलाव", "Market-price variation":"बाज़ार कीमतों में बदलाव", "Post-harvest loss":"कटाई के बाद नुकसान",
    },
    "Kannada": {
        "Agriculture":"ಕೃಷಿ", "Livestock":"ಪಶುಸಂಗೋಪನೆ", "Aquaculture":"ಮೀನುಗಾರಿಕೆ", "Food Processing":"ಆಹಾರ ಸಂಸ್ಕರಣೆ", "Services":"ಸೇವೆಗಳು", "Retail":"ಚಿಲ್ಲರೆ",
        "Crop Cultivation":"ಬೆಳೆ ಕೃಷಿ", "Vegetable Cultivation":"ತರಕಾರಿ ಕೃಷಿ", "Fruit Cultivation":"ಹಣ್ಣು ಕೃಷಿ", "Spice Cultivation":"ಮಸಾಲೆ ಕೃಷಿ", "Floriculture":"ಹೂ ಬೆಳೆ",
        "Poultry Farming":"ಕೋಳಿ ಸಾಕಣೆ", "Dairy Farming":"ಹೈನುಗಾರಿಕೆ", "Goat Farming":"ಮೇಕೆ ಸಾಕಣೆ", "Sheep Farming":"ಕುರಿ ಸಾಕಣೆ", "Fish Farming":"ಮೀನು ಸಾಕಣೆ",
        "Kharif":"ಖರೀಫ್", "Rabi":"ರಬಿ", "Summer":"ಬೇಸಿಗೆ", "None":"ಇಲ್ಲ", "Low":"ಕಡಿಮೆ", "Medium":"ಮಧ್ಯಮ", "High":"ಹೆಚ್ಚು", "Poor":"ಕಡಿಮೆ", "Moderate":"ಮಧ್ಯಮ", "Good":"ಉತ್ತಮ", "No":"ಇಲ್ಲ", "Partial":"ಭಾಗಶಃ", "Yes":"ಹೌದು", "Shared":"ಹಂಚಿಕೆ", "Available":"ಲಭ್ಯ", "Reliable":"ವಿಶ್ವಾಸಾರ್ಹ", "Rain-fed":"ಮಳೆ ಆಧಾರಿತ", "Limited":"ಸೀಮಿತ", "Beginner":"ಆರಂಭಿಕ", "Some experience":"ಸ್ವಲ್ಪ ಅನುಭವ", "Experienced":"ಅನುಭವ ಹೊಂದಿರುವವರು", "Within 3 months":"3 ತಿಂಗಳೊಳಗೆ", "3–6 months":"3–6 ತಿಂಗಳು", "6–12 months":"6–12 ತಿಂಗಳು", "12+ months":"12+ ತಿಂಗಳು",
        "Weather variability":"ಹವಾಮಾನ ಬದಲಾವಣೆ", "Water availability":"ನೀರಿನ ಲಭ್ಯತೆ", "Input-price changes":"ಇನ್‌ಪುಟ್ ಬೆಲೆ ಬದಲಾವಣೆ", "Crop-price changes":"ಬೆಳೆ ಬೆಲೆ ಬದಲಾವಣೆ", "Pest/disease pressure":"ಕೀಟ/ರೋಗದ ಒತ್ತಡ", "Price fluctuations":"ಬೆಲೆ ಏರಿಳಿತ", "Water stress":"ನೀರಿನ ಒತ್ತಡ", "Market-price changes":"ಮಾರುಕಟ್ಟೆ ಬೆಲೆ ಬದಲಾವಣೆ", "Market-price variation":"ಮಾರುಕಟ್ಟೆ ಬೆಲೆ ವ್ಯತ್ಯಾಸ", "Post-harvest loss":"ಕೊಯ್ಲಿನ ನಂತರದ ನಷ್ಟ",
    }
}
for _lang,_map in BUSINESS_DISPLAY_TR.items():
    TEXT[_lang].update(_map)


# Additional dynamic-screen translations.
DYNAMIC_TR = {
 "Hindi": {
  "High Risk":"उच्च जोखिम","Medium Risk":"मध्यम जोखिम","Low Risk":"कम जोखिम","item(s)":"आइटम", "identified":"पहचाने गए",
  "Risk distribution is recalculated from the selected business and the current inputs.":"जोखिम वितरण चुने गए व्यवसाय और वर्तमान जानकारी के आधार पर फिर से गणना किया जाता है।",
  "HIGH RISK":"उच्च जोखिम","MEDIUM RISK":"मध्यम जोखिम","LOW RISK":"कम जोखिम", "Risk":"जोखिम","Level":"स्तर","Impact":"प्रभाव","Control / mitigation":"नियंत्रण / समाधान","Priority gaps":"प्राथमिकता अंतराल","Gap":"अंतराल","Action":"कार्रवाई",
  "No risk rules were triggered for the current business profile. Continue routine monitoring before scaling.":"वर्तमान व्यवसाय प्रोफ़ाइल के लिए कोई जोखिम नियम सक्रिय नहीं हुआ। विस्तार से पहले नियमित निगरानी जारी रखें।",
  "No configured risk items were returned for this activity.":"इस गतिविधि के लिए कोई कॉन्फ़िगर किया गया जोखिम नहीं मिला।",
  "Biological, climatic and operational risks should be actively managed before scaling.":"विस्तार से पहले जैविक, जलवायु और संचालन संबंधी जोखिमों का सक्रिय प्रबंधन करें।",
  "Species / Variety / Product Selection":"प्रजाति / किस्म / उत्पाद चयन","Execution Roadmap":"कार्यान्वयन रोडमैप","Market & Advisory":"बाज़ार और मार्गदर्शन","Risk Control":"जोखिम नियंत्रण","Financial Benchmarks":"वित्तीय मानदंड","Schemes":"योजनाएँ",
  "CAPEX Required":"आवश्यक CAPEX","Break-Even Timeline":"ब्रेक-ईवन समयसीमा","Feasibility Score":"व्यवहार्यता स्कोर","Monthly Operating Cost":"मासिक संचालन लागत",
  "Current input / configured estimate":"वर्तमान जानकारी / कॉन्फ़िगर किया गया अनुमान","Indicative model estimate":"संकेतात्मक मॉडल अनुमान","Adaptive score from available inputs":"उपलब्ध जानकारी से अनुकूलित स्कोर","Indicative, scale-dependent":"संकेतात्मक, पैमाने पर निर्भर",
  "Selection":"चयन","Market & Advisory":"बाज़ार और मार्गदर्शन","Risk Control":"जोखिम नियंत्रण","Financial Benchmarks":"वित्तीय मानदंड",
  "Strategic fit: combine at least one B2B route with a direct or diversified selling channel where the business model allows it.":"रणनीतिक मेल: जहाँ व्यवसाय मॉडल अनुमति देता है, वहाँ कम से कम एक B2B मार्ग को प्रत्यक्ष या विविध बिक्री चैनल के साथ जोड़ें।",
  "Biological, climatic and operational risks should be actively managed before scaling.":"विस्तार से पहले जैविक, जलवायु और संचालन संबंधी जोखिमों का सक्रिय प्रबंधन करें।",
  "Success benchmark: complete a pilot with recorded unit cost, output/service volume, realized selling price, wastage/mortality where relevant, and customer acquisition cost before expanding.":"सफलता मानदंड: विस्तार से पहले दर्ज इकाई लागत, उत्पादन/सेवा मात्रा, वास्तविक बिक्री मूल्य, जहाँ लागू हो वहाँ बर्बादी/मृत्यु दर और ग्राहक प्राप्ति लागत के साथ पायलट पूरा करें।",
  "Practical Decision Check":"व्यावहारिक निर्णय जाँच","Several currently entered conditions support feasibility. Validate supplier quotes, operating costs and buyer demand before scaling.":"वर्तमान में दर्ज कई स्थितियाँ व्यवहार्यता का समर्थन करती हैं। विस्तार से पहले आपूर्तिकर्ता दर, संचालन लागत और खरीदार मांग सत्यापित करें।",
  "The current assessment is mixed. Close the highest-impact gaps and test a smaller pilot before committing the full investment.":"वर्तमान आकलन मिश्रित है। सबसे अधिक प्रभाव वाले अंतराल बंद करें और पूरी पूंजी लगाने से पहले छोटा पायलट करें।",
  "Several configured conditions are weak. Address the highest-impact gaps first and reassess before committing the full investment.":"कई कॉन्फ़िगर की गई स्थितियाँ कमजोर हैं। पहले सबसे अधिक प्रभाव वाले अंतराल सुधारें और पूरी पूंजी लगाने से पहले पुनः आकलन करें।",
  "High potential impact":"उच्च संभावित प्रभाव","Moderate potential impact":"मध्यम संभावित प्रभाव","Lower potential impact":"कम संभावित प्रभाव","Potential impact":"संभावित प्रभाव",
 },
 "Kannada": {
  "High Risk":"ಹೆಚ್ಚಿನ ಅಪಾಯ","Medium Risk":"ಮಧ್ಯಮ ಅಪಾಯ","Low Risk":"ಕಡಿಮೆ ಅಪಾಯ","item(s)":"ಅಂಶಗಳು","identified":"ಗುರುತಿಸಲಾಗಿದೆ",
  "Risk distribution is recalculated from the selected business and the current inputs.":"ಅಪಾಯ ವಿತರಣೆ ಆಯ್ಕೆ ಮಾಡಿದ ವ್ಯವಹಾರ ಮತ್ತು ಪ್ರಸ್ತುತ ಮಾಹಿತಿಯ ಆಧಾರದ ಮೇಲೆ ಮರುಗಣಿಸಲಾಗುತ್ತದೆ.",
  "HIGH RISK":"ಹೆಚ್ಚಿನ ಅಪಾಯ","MEDIUM RISK":"ಮಧ್ಯಮ ಅಪಾಯ","LOW RISK":"ಕಡಿಮೆ ಅಪಾಯ","Risk":"ಅಪಾಯ","Level":"ಮಟ್ಟ","Impact":"ಪರಿಣಾಮ","Control / mitigation":"ನಿಯಂತ್ರಣ / ಪರಿಹಾರ","Priority gaps":"ಆದ್ಯತಾ ಅಂತರಗಳು","Gap":"ಅಂತರ","Action":"ಕ್ರಮ",
  "No risk rules were triggered for the current business profile. Continue routine monitoring before scaling.":"ಪ್ರಸ್ತುತ ವ್ಯವಹಾರ ಪ್ರೊಫೈಲ್‌ಗೆ ಯಾವುದೇ ಅಪಾಯ ನಿಯಮಗಳು ಸಕ್ರಿಯವಾಗಿಲ್ಲ. ವಿಸ್ತರಣೆಗೆ ಮೊದಲು ನಿಯಮಿತ ಮೇಲ್ವಿಚಾರಣೆ ಮುಂದುವರಿಸಿ.",
  "No configured risk items were returned for this activity.":"ಈ ಚಟುವಟಿಕೆಗೆ ಯಾವುದೇ ಕಾನ್ಫಿಗರ್ ಮಾಡಿದ ಅಪಾಯ ಅಂಶಗಳು ದೊರೆಯಲಿಲ್ಲ.",
  "Biological, climatic and operational risks should be actively managed before scaling.":"ವಿಸ್ತರಣೆಗೆ ಮೊದಲು ಜೈವಿಕ, ಹವಾಮಾನ ಮತ್ತು ಕಾರ್ಯಾಚರಣಾ ಅಪಾಯಗಳನ್ನು ಸಕ್ರಿಯವಾಗಿ ನಿರ್ವಹಿಸಬೇಕು.",
  "Species / Variety / Product Selection":"ಜಾತಿ / ತಳಿ / ಉತ್ಪನ್ನ ಆಯ್ಕೆ","Execution Roadmap":"ಕಾರ್ಯಗತಗೊಳಿಸುವಿಕೆ ಮಾರ್ಗಸೂಚಿ","Market & Advisory":"ಮಾರುಕಟ್ಟೆ ಮತ್ತು ಮಾರ್ಗದರ್ಶನ","Risk Control":"ಅಪಾಯ ನಿಯಂತ್ರಣ","Financial Benchmarks":"ಹಣಕಾಸು ಮಾನದಂಡಗಳು","Schemes":"ಯೋಜನೆಗಳು",
  "CAPEX Required":"ಅಗತ್ಯ CAPEX","Break-Even Timeline":"ಬ್ರೇಕ್-ಈವನ್ ಸಮಯಪಟ್ಟಿ","Feasibility Score":"ಕಾರ್ಯಸಾಧ್ಯತಾ ಅಂಕ","Monthly Operating Cost":"ಮಾಸಿಕ ಕಾರ್ಯಾಚರಣಾ ವೆಚ್ಚ",
  "Current input / configured estimate":"ಪ್ರಸ್ತುತ ಮಾಹಿತಿ / ಕಾನ್ಫಿಗರ್ ಮಾಡಿದ ಅಂದಾಜು","Indicative model estimate":"ಸೂಚಕ ಮಾದರಿ ಅಂದಾಜು","Adaptive score from available inputs":"ಲಭ್ಯ ಮಾಹಿತಿಯಿಂದ ಹೊಂದಿಕೊಳ್ಳುವ ಅಂಕ","Indicative, scale-dependent":"ಸೂಚಕ, ಪ್ರಮಾಣದ ಮೇಲೆ ಅವಲಂಬಿತ",
  "Selection":"ಆಯ್ಕೆ","Market & Advisory":"ಮಾರುಕಟ್ಟೆ ಮತ್ತು ಮಾರ್ಗದರ್ಶನ","Risk Control":"ಅಪಾಯ ನಿಯಂತ್ರಣ","Financial Benchmarks":"ಹಣಕಾಸು ಮಾನದಂಡಗಳು",
  "Strategic fit: combine at least one B2B route with a direct or diversified selling channel where the business model allows it.":"ತಂತ್ರಾತ್ಮಕ ಹೊಂದಾಣಿಕೆ: ವ್ಯವಹಾರ ಮಾದರಿ ಅನುಮತಿಸಿದಲ್ಲಿ ಕನಿಷ್ಠ ಒಂದು B2B ಮಾರ್ಗವನ್ನು ನೇರ ಅಥವಾ ವೈವಿಧ್ಯಮಯ ಮಾರಾಟ ಚಾನಲ್‌ನೊಂದಿಗೆ ಸಂಯೋಜಿಸಿ.",
  "Biological, climatic and operational risks should be actively managed before scaling.":"ವಿಸ್ತರಣೆಗೆ ಮೊದಲು ಜೈವಿಕ, ಹವಾಮಾನ ಮತ್ತು ಕಾರ್ಯಾಚರಣಾ ಅಪಾಯಗಳನ್ನು ಸಕ್ರಿಯವಾಗಿ ನಿರ್ವಹಿಸಬೇಕು.",
  "Success benchmark: complete a pilot with recorded unit cost, output/service volume, realized selling price, wastage/mortality where relevant, and customer acquisition cost before expanding.":"ಯಶಸ್ಸಿನ ಮಾನದಂಡ: ವಿಸ್ತರಿಸುವ ಮೊದಲು ಘಟಕ ವೆಚ್ಚ, ಉತ್ಪಾದನೆ/ಸೇವಾ ಪ್ರಮಾಣ, ನಿಜವಾದ ಮಾರಾಟ ಬೆಲೆ, ಅನ್ವಯಿಸಿದಲ್ಲಿ ನಷ್ಟ/ಸಾವು ಪ್ರಮಾಣ ಮತ್ತು ಗ್ರಾಹಕ ಗಳಿಕೆ ವೆಚ್ಚವನ್ನು ದಾಖಲಿಸಿದ ಪೈಲಟ್ ಪೂರ್ಣಗೊಳಿಸಿ.",
  "Practical Decision Check":"ಪ್ರಾಯೋಗಿಕ ನಿರ್ಧಾರ ಪರಿಶೀಲನೆ","Several currently entered conditions support feasibility. Validate supplier quotes, operating costs and buyer demand before scaling.":"ಪ್ರಸ್ತುತ ನಮೂದಿಸಿದ ಹಲವು ಪರಿಸ್ಥಿತಿಗಳು ಕಾರ್ಯಸಾಧ್ಯತೆಯನ್ನು ಬೆಂಬಲಿಸುತ್ತವೆ. ವಿಸ್ತರಣೆಗೆ ಮೊದಲು ಪೂರೈಕೆದಾರರ ದರ, ಕಾರ್ಯಾಚರಣಾ ವೆಚ್ಚ ಮತ್ತು ಖರೀದಿದಾರರ ಬೇಡಿಕೆಯನ್ನು ಪರಿಶೀಲಿಸಿ.",
  "The current assessment is mixed. Close the highest-impact gaps and test a smaller pilot before committing the full investment.":"ಪ್ರಸ್ತುತ ಮೌಲ್ಯಮಾಪನ ಮಿಶ್ರವಾಗಿದೆ. ಹೆಚ್ಚಿನ ಪರಿಣಾಮದ ಅಂತರಗಳನ್ನು ಮುಚ್ಚಿ, ಸಂಪೂರ್ಣ ಹೂಡಿಕೆಗೆ ಮೊದಲು ಸಣ್ಣ ಪೈಲಟ್ ಪರೀಕ್ಷಿಸಿ.",
  "Several configured conditions are weak. Address the highest-impact gaps first and reassess before committing the full investment.":"ಹಲವು ಕಾನ್ಫಿಗರ್ ಮಾಡಿದ ಪರಿಸ್ಥಿತಿಗಳು ದುರ್ಬಲವಾಗಿವೆ. ಹೆಚ್ಚಿನ ಪರಿಣಾಮದ ಅಂತರಗಳನ್ನು ಮೊದಲು ಸರಿಪಡಿಸಿ ಮತ್ತು ಸಂಪೂರ್ಣ ಹೂಡಿಕೆಗೆ ಮೊದಲು ಮರುಮೌಲ್ಯಮಾಪನ ಮಾಡಿ.",
  "High potential impact":"ಹೆಚ್ಚಿನ ಸಾಧ್ಯ ಪರಿಣಾಮ","Moderate potential impact":"ಮಧ್ಯಮ ಸಾಧ್ಯ ಪರಿಣಾಮ","Lower potential impact":"ಕಡಿಮೆ ಸಾಧ್ಯ ಪರಿಣಾಮ","Potential impact":"ಸಂಭಾವ್ಯ ಪರಿಣಾಮ",
 }
}
for _lang,_map in DYNAMIC_TR.items():
    TEXT[_lang].update(_map)

FIELD_UI_TR = {
 "Hindi": {
  "Water availability":"पानी की उपलब्धता","Labour":"श्रमिक","Investment":"निवेश","Market access":"बाज़ार तक पहुँच","Experience":"अनुभव","Electricity":"बिजली","Housing/shed":"आवास/शेड","Feed availability":"चारे की उपलब्धता","Veterinary access":"पशु चिकित्सा सहायता","Fodder availability":"चारा उपलब्धता","Grazing/feed availability":"चराई/चारा उपलब्धता",
  "Land area (acres)":"भूमि क्षेत्रफल (एकड़)","Land/covered area (acres)":"भूमि/कवर क्षेत्रफल (एकड़)","Season":"मौसम","Irrigation":"सिंचाई","Soil test available":"मिट्टी परीक्षण उपलब्ध","Available labour (people)":"उपलब्ध श्रमिक (संख्या)","Available investment (₹)":"उपलब्ध निवेश (₹)","Target time to income":"आय प्राप्ति का लक्ष्य समय","Risk preference":"जोखिम प्राथमिकता","Transport available":"परिवहन उपलब्ध","Storage available":"भंडारण उपलब्ध","Can wait for longer establishment period":"लंबी स्थापना अवधि की प्रतीक्षा कर सकते हैं",
  "Number of birds planned":"नियोजित पक्षियों की संख्या","Suitable shed available":"उपयुक्त शेड उपलब्ध","Available shed area (sq ft)":"उपलब्ध शेड क्षेत्र (वर्ग फुट)","Experience":"अनुभव","Veterinary support access":"पशु चिकित्सा सहायता तक पहुँच","Number of animals planned":"नियोजित पशुओं की संख्या","Animal type":"पशु प्रकार","Milking/chilling equipment":"दूध निकालने/ठंडा करने के उपकरण","Milk market access":"दूध बाज़ार तक पहुँच","Number of goats planned":"नियोजित बकरियों की संख्या","Goat shed available":"बकरी शेड उपलब्ध","Grazing/feed availability":"चराई/चारा उपलब्धता","Number of sheep planned":"नियोजित भेड़ों की संख्या","Sheep shed available":"भेड़ शेड उपलब्ध",
 },
 "Kannada": {
  "Water availability":"ನೀರಿನ ಲಭ್ಯತೆ","Labour":"ಕಾರ್ಮಿಕರು","Investment":"ಹೂಡಿಕೆ","Market access":"ಮಾರುಕಟ್ಟೆ ಪ್ರವೇಶ","Experience":"ಅನುಭವ","Electricity":"ವಿದ್ಯುತ್","Housing/shed":"ವಸತಿ/ಶೆಡ್","Feed availability":"ಆಹಾರ ಲಭ್ಯತೆ","Veterinary access":"ಪಶುವೈದ್ಯಕೀಯ ಪ್ರವೇಶ","Fodder availability":"ಮೇವು ಲಭ್ಯತೆ","Grazing/feed availability":"ಮೇಯಿಸುವಿಕೆ/ಮೇವು ಲಭ್ಯತೆ",
  "Land area (acres)":"ಭೂಮಿ ವಿಸ್ತೀರ್ಣ (ಎಕರೆ)","Land/covered area (acres)":"ಭೂಮಿ/ಆವರಿತ ವಿಸ್ತೀರ್ಣ (ಎಕರೆ)","Season":"ಋತು","Irrigation":"ನೀರಾವರಿ","Soil test available":"ಮಣ್ಣು ಪರೀಕ್ಷೆ ಲಭ್ಯ","Available labour (people)":"ಲಭ್ಯವಿರುವ ಕಾರ್ಮಿಕರು (ಸಂಖ್ಯೆ)","Available investment (₹)":"ಲಭ್ಯವಿರುವ ಹೂಡಿಕೆ (₹)","Target time to income":"ಆದಾಯದ ಗುರಿ ಸಮಯ","Risk preference":"ಅಪಾಯ ಆದ್ಯತೆ","Transport available":"ಸಾರಿಗೆ ಲಭ್ಯ","Storage available":"ಸಂಗ್ರಹಣೆ ಲಭ್ಯ","Can wait for longer establishment period":"ದೀರ್ಘ ಸ್ಥಾಪನಾ ಅವಧಿಗಾಗಿ ಕಾಯಬಹುದು",
  "Number of birds planned":"ಯೋಜಿತ ಪಕ್ಷಿಗಳ ಸಂಖ್ಯೆ","Suitable shed available":"ಸೂಕ್ತ ಶೆಡ್ ಲಭ್ಯ","Available shed area (sq ft)":"ಲಭ್ಯವಿರುವ ಶೆಡ್ ವಿಸ್ತೀರ್ಣ (ಚದರ ಅಡಿ)","Veterinary support access":"ಪಶುವೈದ್ಯಕೀಯ ನೆರವು ಪ್ರವೇಶ","Number of animals planned":"ಯೋಜಿತ ಪ್ರಾಣಿಗಳ ಸಂಖ್ಯೆ","Animal type":"ಪ್ರಾಣಿ ಪ್ರಕಾರ","Milking/chilling equipment":"ಹಾಲು ಹೀರುವ/ತಂಪುಗೊಳಿಸುವ ಉಪಕರಣ", "Milk market access":"ಹಾಲು ಮಾರುಕಟ್ಟೆ ಪ್ರವೇಶ","Number of goats planned":"ಯೋಜಿತ ಮೇಕೆಗಳ ಸಂಖ್ಯೆ","Goat shed available":"ಮೇಕೆ ಶೆಡ್ ಲಭ್ಯ","Number of sheep planned":"ಯೋಜಿತ ಕುರಿಗಳ ಸಂಖ್ಯೆ","Sheep shed available":"ಕುರಿ ಶೆಡ್ ಲಭ್ಯ",
 }
}
for _lang,_map in FIELD_UI_TR.items():
    TEXT[_lang].update(_map)


RISK_UI_TR = {
 "Hindi": {
  "Market-access risk":"बाज़ार पहुँच जोखिम","Capital risk":"पूंजी जोखिम","Execution-capital risk":"कार्यान्वयन-पूंजी जोखिम","Experience / execution risk":"अनुभव / कार्यान्वयन जोखिम","Labour-availability risk":"श्रमिक उपलब्धता जोखिम","Water-availability risk":"पानी उपलब्धता जोखिम","Irrigation reliability risk":"सिंचाई विश्वसनीयता जोखिम","Housing risk":"आवास जोखिम","Animal-health risk":"पशु स्वास्थ्य जोखिम","Feed / fodder cost risk":"चारा लागत जोखिम","Disease / mortality risk":"रोग / मृत्यु जोखिम","Post-harvest / transport risk":"कटाई के बाद / परिवहन जोखिम","Storage risk":"भंडारण जोखिम","Soil-information risk":"मिट्टी जानकारी जोखिम","Time-to-income mismatch":"आय-समय असंगति जोखिम","Biological health risk":"जैविक स्वास्थ्य जोखिम","Input-cost risk":"इनपुट लागत जोखिम","Price risk":"कीमत जोखिम","Biological crop risk":"जैविक फसल जोखिम","Climate risk":"जलवायु जोखिम","Water-quality risk":"पानी गुणवत्ता जोखिम","Perishability risk":"शीघ्र खराब होने का जोखिम","Equipment downtime risk":"उपकरण बंद रहने का जोखिम"
 },
 "Kannada": {
  "Market-access risk":"ಮಾರುಕಟ್ಟೆ ಪ್ರವೇಶ ಅಪಾಯ","Capital risk":"ಬಂಡವಾಳ ಅಪಾಯ","Execution-capital risk":"ಕಾರ್ಯಗತಗೊಳಿಸುವಿಕೆ-ಬಂಡವಾಳ ಅಪಾಯ","Experience / execution risk":"ಅನುಭವ / ಕಾರ್ಯಗತಗೊಳಿಸುವಿಕೆ ಅಪಾಯ","Labour-availability risk":"ಕಾರ್ಮಿಕ ಲಭ್ಯತೆ ಅಪಾಯ","Water-availability risk":"ನೀರಿನ ಲಭ್ಯತೆ ಅಪಾಯ","Irrigation reliability risk":"ನೀರಾವರಿ ವಿಶ್ವಾಸಾರ್ಹತೆ ಅಪಾಯ","Housing risk":"ವಸತಿ ಅಪಾಯ","Animal-health risk":"ಪ್ರಾಣಿ ಆರೋಗ್ಯ ಅಪಾಯ","Feed / fodder cost risk":"ಆಹಾರ / ಮೇವು ವೆಚ್ಚದ ಅಪಾಯ","Disease / mortality risk":"ರೋಗ / ಸಾವು ಅಪಾಯ","Post-harvest / transport risk":"ಕೊಯ್ಲಿನ ನಂತರ / ಸಾರಿಗೆ ಅಪಾಯ","Storage risk":"ಸಂಗ್ರಹಣೆ ಅಪಾಯ","Soil-information risk":"ಮಣ್ಣಿನ ಮಾಹಿತಿ ಅಪಾಯ","Time-to-income mismatch":"ಆದಾಯ-ಸಮಯ ಅಸಂಗತತೆ ಅಪಾಯ","Biological health risk":"ಜೈವಿಕ ಆರೋಗ್ಯ ಅಪಾಯ","Input-cost risk":"ಇನ್‌ಪುಟ್ ವೆಚ್ಚದ ಅಪಾಯ","Price risk":"ಬೆಲೆ ಅಪಾಯ","Biological crop risk":"ಜೈವಿಕ ಬೆಳೆ ಅಪಾಯ","Climate risk":"ಹವಾಮಾನ ಅಪಾಯ","Water-quality risk":"ನೀರಿನ ಗುಣಮಟ್ಟದ ಅಪಾಯ","Perishability risk":"ಶೀಘ್ರ ಹಾಳಾಗುವ ಅಪಾಯ","Equipment downtime risk":"ಉಪಕರಣ ಸ್ಥಗಿತ ಅಪಾಯ"
 }
}
for _lang,_map in RISK_UI_TR.items():
    TEXT[_lang].update(_map)

DATA_TR = {
    "Hindi": {
        "Increasing":"बढ़ रहा है","Stable":"स्थिर","Decreasing":"घट रहा है",
        "Vegetable":"सब्ज़ी","Leafy":"पत्तेदार","Cereal":"अनाज","Oilseed":"तिलहन","Pulse":"दलहन","Commercial":"व्यावसायिक","Spice":"मसाला","Horticulture":"बागवानी","Fruit":"फल",
        "Tomato":"टमाटर","Onion":"प्याज़","Potato":"आलू","Carrot":"गाजर","Beans":"बीन्स","Brinjal":"बैंगन","Cabbage":"पत्तागोभी","Cauliflower":"फूलगोभी","Capsicum":"शिमला मिर्च","Green Chilli":"हरी मिर्च","Lady Finger":"भिंडी","Bottle Gourd":"लौकी","Bitter Gourd":"करेला","Cucumber":"खीरा","Pumpkin":"कद्दू","Drumstick":"सहजन","Peas":"मटर","Beetroot":"चुकंदर","Radish":"मूली","Spinach":"पालक","Coriander":"धनिया","Fenugreek Leaves":"मेथी","Maize":"मक्का","Wheat":"गेहूँ","Rice":"चावल","Ragi":"रागी","Jowar":"ज्वार","Bajra":"बाजरा","Groundnut":"मूंगफली","Sunflower":"सूरजमुखी","Soybean":"सोयाबीन","Tur":"तूर दाल","Green Gram":"मूंग","Black Gram":"उड़द","Bengal Gram":"चना","Cotton":"कपास","Sugarcane":"गन्ना","Turmeric":"हल्दी","Chilli":"मिर्च","Ginger":"अदरक","Garlic":"लहसुन","Coconut":"नारियल","Banana":"केला","Mango":"आम","Papaya":"पपीता","Guava":"अमरूद"
    },
    "Kannada": {
        "Increasing":"ಏರಿಕೆ","Stable":"ಸ್ಥಿರ","Decreasing":"ಇಳಿಕೆ",
        "Vegetable":"ತರಕಾರಿ","Leafy":"ಸೊಪ್ಪು","Cereal":"ಧಾನ್ಯ","Oilseed":"ಎಣ್ಣೆಬೀಜ","Pulse":"ಬೇಳೆ","Commercial":"ವಾಣಿಜ್ಯ","Spice":"ಮಸಾಲೆ","Horticulture":"ತೋಟಗಾರಿಕೆ","Fruit":"ಹಣ್ಣು",
        "Tomato":"ಟೊಮ್ಯಾಟೊ","Onion":"ಈರುಳ್ಳಿ","Potato":"ಆಲೂಗಡ್ಡೆ","Carrot":"ಕ್ಯಾರೆಟ್","Beans":"ಬೀನ್ಸ್","Brinjal":"ಬದನೆಕಾಯಿ","Cabbage":"ಎಲೆಕೋಸು","Cauliflower":"ಹೂಕೋಸು","Capsicum":"ಕ್ಯಾಪ್ಸಿಕಂ","Green Chilli":"ಹಸಿರು ಮೆಣಸಿನಕಾಯಿ","Lady Finger":"ಬೆಂಡೆಕಾಯಿ","Bottle Gourd":"ಸೋರೆಕಾಯಿ","Bitter Gourd":"ಹಾಗಲಕಾಯಿ","Cucumber":"ಸೌತೆಕಾಯಿ","Pumpkin":"ಕುಂಬಳಕಾಯಿ","Drumstick":"ನುಗ್ಗೆಕಾಯಿ","Peas":"ಬಟಾಣಿ","Beetroot":"ಬೀಟ್ರೂಟ್","Radish":"ಮೂಲಂಗಿ","Spinach":"ಪಾಲಕ್ ಸೊಪ್ಪು","Coriander":"ಕೊತ್ತಂಬರಿ ಸೊಪ್ಪು","Fenugreek Leaves":"ಮೆಂತ್ಯ ಸೊಪ್ಪು","Maize":"ಮೆಕ್ಕೆಜೋಳ","Wheat":"ಗೋಧಿ","Rice":"ಅಕ್ಕಿ","Ragi":"ರಾಗಿ","Jowar":"ಜೋಳ","Bajra":"ಸಜ್ಜೆ","Groundnut":"ಕಡಲೆಕಾಯಿ","Sunflower":"ಸೂರ್ಯಕಾಂತಿ","Soybean":"ಸೋಯಾಬೀನ್","Tur":"ತೊಗರಿ","Green Gram":"ಹೆಸರುಕಾಳು","Black Gram":"ಉದ್ದು","Bengal Gram":"ಕಡಲೆ","Cotton":"ಹತ್ತಿ","Sugarcane":"ಕಬ್ಬು","Turmeric":"ಅರಿಶಿನ","Chilli":"ಮೆಣಸಿನಕಾಯಿ","Ginger":"ಶುಂಠಿ","Garlic":"ಬೆಳ್ಳುಳ್ಳಿ","Coconut":"ತೆಂಗಿನಕಾಯಿ","Banana":"ಬಾಳೆಹಣ್ಣು","Mango":"ಮಾವು","Papaya":"ಪಪ್ಪಾಯಿ","Guava":"ಸೀಬೆಹಣ್ಣು"
    }
}

def tr_data(value):
    lang = _current_language()
    return DATA_TR.get(lang, {}).get(value, value)

def tr(key, **kwargs):
    lang = _current_language()
    value = TEXT.get(lang, TEXT["English"]).get(key, TEXT["English"].get(key, key))
    return value.format(**kwargs) if kwargs else value

# ------------------------------------------------------------
# PLACE NAMES  (English -> (Hindi, Kannada))
# Districts and taluks / towns shown in the location dropdown and everywhere
# a location name appears inside text.
# ------------------------------------------------------------
_GS_PLACE_PAIRS = {
    # districts
    "Bagalkot": ("बागलकोट", "ಬಾಗಲಕೋಟೆ"),
    "Ballari": ("बल्लारी", "ಬಳ್ಳಾರಿ"),
    "Belagavi": ("बेलगावी", "ಬೆಳಗಾವಿ"),
    "Bengaluru Rural": ("बेंगलुरु ग्रामीण", "ಬೆಂಗಳೂರು ಗ್ರಾಮಾಂತರ"),
    "Bengaluru Urban": ("बेंगलुरु शहरी", "ಬೆಂಗಳೂರು ನಗರ"),
    "Bengaluru": ("बेंगलुरु", "ಬೆಂಗಳೂರು"),
    "Bidar": ("बीदर", "ಬೀದರ್"),
    "Chamarajanagar": ("चामराजनगर", "ಚಾಮರಾಜನಗರ"),
    "Chikballapur": ("चिक्कबल्लापुर", "ಚಿಕ್ಕಬಳ್ಳಾಪುರ"),
    "Chikkaballapur": ("चिक्कबल्लापुर", "ಚಿಕ್ಕಬಳ್ಳಾಪುರ"),
    "Chikkamagaluru": ("चिक्कमगलूरु", "ಚಿಕ್ಕಮಗಳೂರು"),
    "Chitradurga": ("चित्रदुर्ग", "ಚಿತ್ರದುರ್ಗ"),
    "Dakshina Kannada": ("दक्षिण कन्नड़", "ದಕ್ಷಿಣ ಕನ್ನಡ"),
    "Dakshin Kannada": ("दक्षिण कन्नड़", "ದಕ್ಷಿಣ ಕನ್ನಡ"),
    "Davanagere": ("दावणगेरे", "ದಾವಣಗೆರೆ"),
    "Dharwad": ("धारवाड़", "ಧಾರವಾಡ"),
    "Gadag": ("गदग", "ಗದಗ"),
    "Hassan": ("हासन", "ಹಾಸನ"),
    "Haveri": ("हावेरी", "ಹಾವೇರಿ"),
    "Kalaburagi": ("कलबुर्गी", "ಕಲಬುರಗಿ"),
    "Kodagu": ("कोडागु", "ಕೊಡಗು"),
    "Kolar": ("कोलार", "ಕೋಲಾರ"),
    "Koppal": ("कोप्पल", "ಕೊಪ್ಪಳ"),
    "Mandya": ("मंड्या", "ಮಂಡ್ಯ"),
    "Mysuru": ("मैसूरु", "ಮೈಸೂರು"),
    "Raichur": ("रायचूर", "ರಾಯಚೂರು"),
    "Ramanagara": ("रामनगर", "ರಾಮನಗರ"),
    "Shivamogga": ("शिवमोगा", "ಶಿವಮೊಗ್ಗ"),
    "Tumakuru": ("तुमकुरु", "ತುಮಕೂರು"),
    "Udupi": ("उडुपी", "ಉಡುಪಿ"),
    "Uttara Kannada": ("उत्तर कन्नड़", "ಉತ್ತರ ಕನ್ನಡ"),
    "Vijayapura": ("विजयपुरा", "ವಿಜಯಪುರ"),
    "Vijayanagara": ("विजयनगर", "ವಿಜಯನಗರ"),
    "Yadgir": ("यादगीर", "ಯಾದಗಿರಿ"),
    # taluks / towns
    "Jamkhandi": ("जमखंडी", "ಜಮಖಂಡಿ"),
    "Badami": ("बादामी", "ಬಾದಾಮಿ"),
    "Hosapete": ("होसपेटे", "ಹೊಸಪೇಟೆ"),
    "Sandur": ("संडूर", "ಸಂಡೂರು"),
    "Gokak": ("गोकाक", "ಗೋಕಾಕ್"),
    "Chikkodi": ("चिक्कोडी", "ಚಿಕ್ಕೋಡಿ"),
    "Athani": ("अथणी", "ಅಥಣಿ"),
    "Nelamangala": ("नेलमंगला", "ನೆಲಮಂಗಲ"),
    "Devanahalli": ("देवनहल्ली", "ದೇವನಹಳ್ಳಿ"),
    "Doddaballapura": ("दोड्डबल्लापुर", "ದೊಡ್ಡಬಳ್ಳಾಪುರ"),
    "Anekal": ("आनेकल", "ಆನೇಕಲ್"),
    "Humnabad": ("हुमनाबाद", "ಹುಮನಾಬಾದ್"),
    "Basavakalyan": ("बसवकल्याण", "ಬಸವಕಲ್ಯಾಣ"),
    "Kollegal": ("कोल्लेगाल", "ಕೊಳ್ಳೇಗಾಲ"),
    "Gundlupet": ("गुंडलुपेट", "ಗುಂಡ್ಲುಪೇಟೆ"),
    "Chikballapur Town": ("चिक्कबल्लापुर नगर", "ಚಿಕ್ಕಬಳ್ಳಾಪುರ ಪಟ್ಟಣ"),
    "Sringeri": ("शृंगेरी", "ಶೃಂಗೇರಿ"),
    "Mudigere": ("मूडिगेरे", "ಮೂಡಿಗೆರೆ"),
    "Kadur": ("कडूर", "ಕಡೂರು"),
    "Hiriyur": ("हिरियूर", "ಹಿರಿಯೂರು"),
    "Challakere": ("चल्लकेरे", "ಚಳ್ಳಕೆರೆ"),
    "Mangaluru": ("मंगलुरु", "ಮಂಗಳೂರು"),
    "Puttur": ("पुत्तूर", "ಪುತ್ತೂರು"),
    "Bantwal": ("बंटवाल", "ಬಂಟ್ವಾಳ"),
    "Harihar": ("हरिहर", "ಹರಿಹರ"),
    "Channagiri": ("चन्नगिरी", "ಚನ್ನಗಿರಿ"),
    "Hubballi": ("हुब्बल्ली", "ಹುಬ್ಬಳ್ಳಿ"),
    "Kalghatgi": ("कलघटगी", "ಕಲಘಟಗಿ"),
    "Ron": ("रोण", "ರೋಣ"),
    "Sakleshpur": ("सकलेशपुर", "ಸಕಲೇಶಪುರ"),
    "Arsikere": ("अरसीकेरे", "ಅರಸೀಕೆರೆ"),
    "Ranebennur": ("राणेबेन्नूर", "ರಾಣೆಬೆನ್ನೂರು"),
    "Shahapur": ("शहापुर", "ಶಹಾಪುರ"),
    "Madikeri": ("मडिकेरी", "ಮಡಿಕೇರಿ"),
    "Virajpet": ("विराजपेट", "ವಿರಾಜಪೇಟೆ"),
    "Malur": ("मालूर", "ಮಾಲೂರು"),
    "Srinivaspur": ("श्रीनिवासपुर", "ಶ್ರೀನಿವಾಸಪುರ"),
    "Gangavati": ("गंगावती", "ಗಂಗಾವತಿ"),
    "Kunigal": ("कुनिगल", "ಕುಣಿಗಲ್"),
    "Pandavapura": ("पांडवपुर", "ಪಾಂಡವಪುರ"),
    "Srirangapatna": ("श्रीरंगपट्टन", "ಶ್ರೀರಂಗಪಟ್ಟಣ"),
    "Hunsur": ("हुणसूर", "ಹುಣಸೂರು"),
    "Nanjangud": ("नंजनगूड", "ನಂಜನಗೂಡು"),
    "Manvi": ("मानवी", "ಮಾನ್ವಿ"),
    "Sindhanur": ("सिंधनूर", "ಸಿಂಧನೂರು"),
    "Channapatna": ("चन्नपट्टण", "ಚನ್ನಪಟ್ಟಣ"),
    "Magadi": ("मागडी", "ಮಾಗಡಿ"),
    "Sagara": ("सागर", "ಸಾಗರ"),
    "Bhadravathi": ("भद्रावती", "ಭದ್ರಾವತಿ"),
    "Tiptur": ("तिपटूर", "ತಿಪಟೂರು"),
    "Kundapura": ("कुंदापुर", "ಕುಂದಾಪುರ"),
    "Karkala": ("कारकल", "ಕಾರ್ಕಳ"),
    "Sirsi": ("शिरसी", "ಶಿರಸಿ"),
    "Karwar": ("कारवार", "ಕಾರವಾರ"),
    "Sindagi": ("सिंदगी", "ಸಿಂದಗಿ"),
    "Indi": ("इंडी", "ಇಂಡಿ"),
}
GS_PLACES_EN = list(_GS_PLACE_PAIRS.keys())
GS_PLACES = {
    "Hindi": {k: v[0] for k, v in _GS_PLACE_PAIRS.items()},
    "Kannada": {k: v[1] for k, v in _GS_PLACE_PAIRS.items()},
}

# ------------------------------------------------------------
# CURATED TRANSLATIONS — interface (English -> (Hindi, Kannada))
# Keys are the English text exactly as the app shows it (emoji / markdown
# prefixes are stripped automatically).  {} = a number or place name.
# ------------------------------------------------------------
_UI_PAIRS = {
    # ---- top bar -------------------------------------------------------
    "English": ("English", "English"),
    "Gram Sahayak": ("ग्राम सहायक", "ಗ್ರಾಮ ಸಹಾಯಕ"),
    "Home": ("होम", "ಮುಖಪುಟ"),
    "Market Prices": ("बाज़ार भाव", "ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳು"),
    "Schemes": ("योजनाएँ", "ಯೋಜನೆಗಳು"),
    "Finance": ("वित्त", "ಹಣಕಾಸು"),
    "Business": ("व्यवसाय", "ವ್ಯವಹಾರ"),
    "Language": ("भाषा", "ಭಾಷೆ"),
    "Location": ("स्थान", "ಸ್ಥಳ"),
    "Navigate": ("नेविगेट करें", "ನ್ಯಾವಿಗೇಟ್ ಮಾಡಿ"),
    "Prototype for rural micro-entrepreneur business guidance": (
        "ग्रामीण सूक्ष्म उद्यमियों के लिए व्यवसाय मार्गदर्शन प्रोटोटाइप",
        "ಗ್ರಾಮೀಣ ಸಣ್ಣ ಉದ್ಯಮಿಗಳಿಗೆ ವ್ಯವಹಾರ ಮಾರ್ಗದರ್ಶನ ಪ್ರೋಟೋಟೈಪ್"),
    "Live state mandi prices": ("कर्नाटक की लाइव मंडी कीमतें", "ಕರ್ನಾಟಕದ ಲೈವ್ ಮಂಡಿ ಬೆಲೆಗಳು"),
    "Rule-based recommendations": ("नियम-आधारित सुझाव", "ನಿಯಮಾಧಾರಿತ ಶಿಫಾರಸುಗಳು"),
    "Verify official scheme information before decisions": (
        "निर्णय से पहले आधिकारिक योजना जानकारी सत्यापित करें", "ನಿರ್ಧಾರಕ್ಕೂ ಮೊದಲು ಅಧಿಕೃತ ಯೋಜನೆ ಮಾಹಿತಿಯನ್ನು ಪರಿಶೀಲಿಸಿ"),

    # ---- home ----------------------------------------------------------
    "Agriculture • Information • Guidance": ("कृषि • जानकारी • मार्गदर्शन", "ಕೃಷಿ • ಮಾಹಿತಿ • ಮಾರ್ಗದರ್ಶನ"),
    "Your Digital Companion for Smarter Farming": (
        "स्मार्ट खेती के लिए आपका डिजिटल साथी", "ಸ್ಮಾರ್ಟ್ ಕೃಷಿಗೆ ನಿಮ್ಮ ಡಿಜಿಟಲ್ ಸಂಗಾತಿ"),
    "Get useful information about crops, market prices, government schemes and financial guidance — all in one place.": (
        "फसलों, बाज़ार भाव, सरकारी योजनाओं और वित्तीय मार्गदर्शन की उपयोगी जानकारी — सब एक ही जगह।",
        "ಬೆಳೆಗಳು, ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳು, ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು ಮತ್ತು ಹಣಕಾಸು ಮಾರ್ಗದರ್ಶನದ ಉಪಯುಕ್ತ ಮಾಹಿತಿ — ಎಲ್ಲವೂ ಒಂದೇ ಸ್ಥಳದಲ್ಲಿ."),
    "Discover Better Farming Information": ("बेहतर खेती की जानकारी पाएँ", "ಉತ್ತಮ ಕೃಷಿ ಮಾಹಿತಿಯನ್ನು ಅನ್ವೇಷಿಸಿ"),
    "Explore crop information and practical agricultural guidance through a simple farmer-friendly interface.": (
        "किसान-अनुकूल सरल इंटरफ़ेस के माध्यम से फसल जानकारी और व्यावहारिक कृषि मार्गदर्शन देखें।",
        "ರೈತ ಸ್ನೇಹಿ ಸರಳ ಇಂಟರ್ಫೇಸ್ ಮೂಲಕ ಬೆಳೆ ಮಾಹಿತಿ ಮತ್ತು ಪ್ರಾಯೋಗಿಕ ಕೃಷಿ ಮಾರ್ಗದರ್ಶನವನ್ನು ನೋಡಿ."),
    "Make Informed Decisions": ("सोच-समझकर निर्णय लें", "ತಿಳಿದುಕೊಂಡು ನಿರ್ಧಾರ ಕೈಗೊಳ್ಳಿ"),
    "Check available mandi prices, explore schemes and use financial guidance to support your next step.": (
        "उपलब्ध मंडी भाव देखें, योजनाएँ खोजें और अपने अगले कदम के लिए वित्तीय मार्गदर्शन का उपयोग करें।",
        "ಲಭ್ಯವಿರುವ ಮಂಡಿ ಬೆಲೆಗಳನ್ನು ನೋಡಿ, ಯೋಜನೆಗಳನ್ನು ಅನ್ವೇಷಿಸಿ ಮತ್ತು ನಿಮ್ಮ ಮುಂದಿನ ಹೆಜ್ಜೆಗೆ ಹಣಕಾಸು ಮಾರ್ಗದರ್ಶನ ಬಳಸಿ."),
    "Explore Gram Sahayak": ("ग्राम सहायक को जानें", "ಗ್ರಾಮ ಸಹಾಯಕವನ್ನು ಅನ್ವೇಷಿಸಿ"),
    "Useful tools gathered in one simple farmer-friendly interface.": (
        "उपयोगी साधन, एक सरल किसान-अनुकूल इंटरफ़ेस में।", "ಉಪಯುಕ್ತ ಸಾಧನಗಳು, ಒಂದೇ ಸರಳ ರೈತ ಸ್ನೇಹಿ ಇಂಟರ್ಫೇಸ್‌ನಲ್ಲಿ."),
    "Crop Information": ("फसल जानकारी", "ಬೆಳೆ ಮಾಹಿತಿ"),
    "Learn about crops and farming practices.": ("फसलों और खेती की पद्धतियों के बारे में जानें।", "ಬೆಳೆಗಳು ಮತ್ತು ಕೃಷಿ ಪದ್ಧತಿಗಳ ಬಗ್ಗೆ ತಿಳಿಯಿರಿ."),
    "Check the latest available mandi prices.": ("उपलब्ध नवीनतम मंडी भाव देखें।", "ಲಭ್ಯವಿರುವ ಇತ್ತೀಚಿನ ಮಂಡಿ ಬೆಲೆಗಳನ್ನು ನೋಡಿ."),
    "Government Schemes": ("सरकारी योजनाएँ", "ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು"),
    "Explore useful government agricultural schemes.": ("उपयोगी सरकारी कृषि योजनाएँ देखें।", "ಉಪಯುಕ್ತ ಸರ್ಕಾರಿ ಕೃಷಿ ಯೋಜನೆಗಳನ್ನು ನೋಡಿ."),
    "Financial Assistant": ("वित्तीय सहायक", "ಹಣಕಾಸು ಸಹಾಯಕ"),
    "Get simple financial guidance for farming.": ("खेती के लिए सरल वित्तीय मार्गदर्शन पाएँ।", "ಕೃಷಿಗೆ ಸರಳ ಹಣಕಾಸು ಮಾರ್ಗದರ್ಶನ ಪಡೆಯಿರಿ."),
    "Farming at a Glance": ("एक नज़र में खेती", "ಒಂದು ನೋಟದಲ್ಲಿ ಕೃಷಿ"),
    "A quick overview using information already available in the app.": (
        "ऐप में पहले से उपलब्ध जानकारी पर आधारित संक्षिप्त सार।", "ಆ್ಯಪ್‌ನಲ್ಲಿ ಈಗಾಗಲೇ ಲಭ್ಯವಿರುವ ಮಾಹಿತಿ ಆಧರಿಸಿದ ಸಂಕ್ಷಿಪ್ತ ನೋಟ."),
    "Crop": ("फसल", "ಬೆಳೆ"),
    "Select in Crop Information": ("फसल जानकारी में चुनें", "ಬೆಳೆ ಮಾಹಿತಿಯಲ್ಲಿ ಆಯ್ಕೆ ಮಾಡಿ"),
    "Market Price": ("बाज़ार भाव", "ಮಾರುಕಟ್ಟೆ ಬೆಲೆ"),
    "Latest available in Market Prices": ("बाज़ार भाव में उपलब्ध नवीनतम", "ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳಲ್ಲಿ ಲಭ್ಯವಿರುವ ಇತ್ತೀಚಿನದು"),
    "Latest available mandi prices": ("उपलब्ध नवीनतम मंडी भाव", "ಲಭ್ಯವಿರುವ ಇತ್ತೀಚಿನ ಮಂಡಿ ಬೆಲೆಗಳು"),
    "Available in the Government Schemes page": ("सरकारी योजनाएँ पृष्ठ में उपलब्ध", "ಸರ್ಕಾರಿ ಯೋಜನೆಗಳ ಪುಟದಲ್ಲಿ ಲಭ್ಯ"),
    "How Gram Sahayak Works": ("ग्राम सहायक कैसे काम करता है", "ಗ್ರಾಮ ಸಹಾಯಕ ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ"),
    "A location-aware digital farm companion: understand → compare → plan → act, with Gram Vaani available for voice guidance in English, Hindi and Kannada.": (
        "स्थान-आधारित डिजिटल कृषि साथी: समझें → तुलना करें → योजना बनाएँ → कार्य करें, और अंग्रेज़ी, हिंदी व कन्नड़ में आवाज़ मार्गदर्शन के लिए ग्राम वाणी।",
        "ಸ್ಥಳಾಧಾರಿತ ಡಿಜಿಟಲ್ ಕೃಷಿ ಸಂಗಾತಿ: ಅರ್ಥಮಾಡಿಕೊಳ್ಳಿ → ಹೋಲಿಸಿ → ಯೋಜಿಸಿ → ಕಾರ್ಯಗತಗೊಳಿಸಿ; ಇಂಗ್ಲಿಷ್, ಹಿಂದಿ ಮತ್ತು ಕನ್ನಡದಲ್ಲಿ ಧ್ವನಿ ಮಾರ್ಗದರ್ಶನಕ್ಕೆ ಗ್ರಾಮ ವಾಣಿ."),
    "Set Your Location": ("अपना स्थान चुनें", "ನಿಮ್ಮ ಸ್ಥಳವನ್ನು ಆಯ್ಕೆಮಾಡಿ"),
    "Choose your location once. Gram Sahayak reuses it for climate context, temperature, water profile, market context and business planning.": (
        "अपना स्थान एक बार चुनें। ग्राम सहायक इसे जलवायु संदर्भ, तापमान, जल प्रोफ़ाइल, बाज़ार संदर्भ और व्यवसाय योजना के लिए दोबारा उपयोग करता है।",
        "ನಿಮ್ಮ ಸ್ಥಳವನ್ನು ಒಮ್ಮೆ ಆಯ್ಕೆಮಾಡಿ. ಗ್ರಾಮ ಸಹಾಯಕವು ಇದನ್ನು ಹವಾಮಾನ ಸಂದರ್ಭ, ತಾಪಮಾನ, ನೀರಿನ ಪ್ರೊಫೈಲ್, ಮಾರುಕಟ್ಟೆ ಸಂದರ್ಭ ಮತ್ತು ವ್ಯವಹಾರ ಯೋಜನೆಗೆ ಮರುಬಳಸುತ್ತದೆ."),
    "Explore the Right Tool": ("सही साधन चुनें", "ಸರಿಯಾದ ಸಾಧನವನ್ನು ಆರಿಸಿ"),
    "Move between Crop Information, Market Prices, Government Schemes, Financial Assistant and Business Recommendation without repeatedly entering your location.": (
        "बार-बार स्थान दर्ज किए बिना फसल जानकारी, बाज़ार भाव, सरकारी योजनाएँ, वित्तीय सहायक और व्यवसाय सुझाव के बीच जाएँ।",
        "ಸ್ಥಳವನ್ನು ಪದೇ ಪದೇ ನಮೂದಿಸದೆ ಬೆಳೆ ಮಾಹಿತಿ, ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳು, ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು, ಹಣಕಾಸು ಸಹಾಯಕ ಮತ್ತು ವ್ಯವಹಾರ ಶಿಫಾರಸಿನ ನಡುವೆ ಸಂಚರಿಸಿ."),
    "Personalise the Assessment": ("आकलन को अपने अनुसार बनाएँ", "ಮೌಲ್ಯಮಾಪನವನ್ನು ನಿಮಗೆ ಹೊಂದಿಸಿ"),
    "Enter only the relevant details. Business Recommendation adds species/variety/product selection and automatically brings location-based temperature into the assessment.": (
        "केवल आवश्यक जानकारी भरें। व्यवसाय सुझाव में प्रजाति/किस्म/उत्पाद का चयन जुड़ता है और स्थान-आधारित तापमान अपने-आप आकलन में आ जाता है।",
        "ಸಂಬಂಧಿತ ವಿವರಗಳನ್ನು ಮಾತ್ರ ನಮೂದಿಸಿ. ವ್ಯವಹಾರ ಶಿಫಾರಸು ಜಾತಿ/ತಳಿ/ಉತ್ಪನ್ನ ಆಯ್ಕೆಯನ್ನು ಸೇರಿಸುತ್ತದೆ ಮತ್ತು ಸ್ಥಳಾಧಾರಿತ ತಾಪಮಾನವನ್ನು ತಾನಾಗಿಯೇ ಮೌಲ್ಯಮಾಪನಕ್ಕೆ ತರುತ್ತದೆ."),
    "Turn Information into Action": ("जानकारी को कार्य में बदलें", "ಮಾಹಿತಿಯನ್ನು ಕ್ರಿಯೆಯಾಗಿ ಪರಿವರ್ತಿಸಿ"),
    "Receive practical outputs: crop/environment matching, mandi information, scheme discovery, financial planning and business roadmaps with risks and next steps.": (
        "व्यावहारिक परिणाम पाएँ: फसल/पर्यावरण मिलान, मंडी जानकारी, योजना खोज, वित्तीय योजना और जोखिम व अगले कदमों के साथ व्यवसाय रोडमैप।",
        "ಪ್ರಾಯೋಗಿಕ ಫಲಿತಾಂಶಗಳನ್ನು ಪಡೆಯಿರಿ: ಬೆಳೆ/ಪರಿಸರ ಹೊಂದಾಣಿಕೆ, ಮಂಡಿ ಮಾಹಿತಿ, ಯೋಜನೆ ಅನ್ವೇಷಣೆ, ಹಣಕಾಸು ಯೋಜನೆ ಮತ್ತು ಅಪಾಯಗಳು ಹಾಗೂ ಮುಂದಿನ ಹಂತಗಳೊಂದಿಗೆ ವ್ಯವಹಾರ ಮಾರ್ಗಸೂಚಿ."),
    "Ask Gram Vaani": ("ग्राम वाणी से पूछें", "ಗ್ರಾಮ ವಾಣಿಯನ್ನು ಕೇಳಿ"),
    "Use the multilingual voice assistant to ask about your location, temperature, crops, markets, schemes, finance or business planning in English, Hindi or Kannada.": (
        "बहुभाषी आवाज़ सहायक से अंग्रेज़ी, हिंदी या कन्नड़ में अपने स्थान, तापमान, फसलों, बाज़ार, योजनाओं, वित्त या व्यवसाय योजना के बारे में पूछें।",
        "ಬಹುಭಾಷಾ ಧ್ವನಿ ಸಹಾಯಕದಿಂದ ಇಂಗ್ಲಿಷ್, ಹಿಂದಿ ಅಥವಾ ಕನ್ನಡದಲ್ಲಿ ನಿಮ್ಮ ಸ್ಥಳ, ತಾಪಮಾನ, ಬೆಳೆಗಳು, ಮಾರುಕಟ್ಟೆ, ಯೋಜನೆಗಳು, ಹಣಕಾಸು ಅಥವಾ ವ್ಯವಹಾರ ಯೋಜನೆ ಬಗ್ಗೆ ಕೇಳಿ."),
    "From Seed to Harvest": ("बीज से कटाई तक", "ಬೀಜದಿಂದ ಕೊಯ್ಲಿನವರೆಗೆ"),
    "Grow Smarter with Gram Sahayak": ("ग्राम सहायक के साथ स्मार्ट खेती करें", "ಗ್ರಾಮ ಸಹಾಯಕದೊಂದಿಗೆ ಜಾಣ್ಮೆಯಿಂದ ಬೆಳೆಯಿರಿ"),
    "Get crop information, market updates, scheme details and financial guidance to support better farming decisions.": (
        "बेहतर खेती निर्णयों के लिए फसल जानकारी, बाज़ार अपडेट, योजना विवरण और वित्तीय मार्गदर्शन पाएँ।",
        "ಉತ್ತಮ ಕೃಷಿ ನಿರ್ಧಾರಗಳಿಗೆ ಬೆಳೆ ಮಾಹಿತಿ, ಮಾರುಕಟ್ಟೆ ಅಪ್‌ಡೇಟ್, ಯೋಜನೆ ವಿವರಗಳು ಮತ್ತು ಹಣಕಾಸು ಮಾರ್ಗದರ್ಶನ ಪಡೆಯಿರಿ."),
    "Market Updates": ("बाज़ार अपडेट", "ಮಾರುಕಟ್ಟೆ ಅಪ್‌ಡೇಟ್‌ಗಳು"),
    "Financial Guidance": ("वित्तीय मार्गदर्शन", "ಹಣಕಾಸು ಮಾರ್ಗದರ್ಶನ"),
    "Built for Farmers": ("किसानों के लिए बनाया गया", "ರೈತರಿಗಾಗಿ ರೂಪಿಸಲಾಗಿದೆ"),
    "Gram Sahayak brings important agricultural information together in a simple and accessible interface.": (
        "ग्राम सहायक महत्वपूर्ण कृषि जानकारी को एक सरल और सुलभ इंटरफ़ेस में एक साथ लाता है।",
        "ಗ್ರಾಮ ಸಹಾಯಕವು ಪ್ರಮುಖ ಕೃಷಿ ಮಾಹಿತಿಯನ್ನು ಸರಳ ಮತ್ತು ಸುಲಭವಾಗಿ ತಲುಪುವ ಇಂಟರ್ಫೇಸ್‌ನಲ್ಲಿ ಒಟ್ಟಿಗೆ ತರುತ್ತದೆ."),
    "Simple to use": ("उपयोग में सरल", "ಬಳಸಲು ಸರಳ"),
    "Agricultural information": ("कृषि जानकारी", "ಕೃಷಿ ಮಾಹಿತಿ"),
    "Government scheme information": ("सरकारी योजना जानकारी", "ಸರ್ಕಾರಿ ಯೋಜನೆ ಮಾಹಿತಿ"),
    "Financial guidance": ("वित्तीय मार्गदर्शन", "ಹಣಕಾಸು ಮಾರ್ಗದರ್ಶನ"),
    "Everything you need, in one place.": ("आपकी ज़रूरत की हर चीज़, एक ही जगह।", "ನಿಮಗೆ ಬೇಕಾದ ಎಲ್ಲವೂ, ಒಂದೇ ಸ್ಥಳದಲ್ಲಿ."),
    "Explore Gram Sahayak and discover useful tools for smarter farming.": (
        "ग्राम सहायक को जानें और स्मार्ट खेती के उपयोगी साधन खोजें।", "ಗ್ರಾಮ ಸಹಾಯಕವನ್ನು ಅನ್ವೇಷಿಸಿ ಮತ್ತು ಜಾಣ ಕೃಷಿಗೆ ಉಪಯುಕ್ತ ಸಾಧನಗಳನ್ನು ಕಂಡುಕೊಳ್ಳಿ."),

    # ---- market prices -------------------------------------------------
    "Live **Karnataka** mandi prices for **{}** ({} district) from the Government of India Open Government Data platform, data.gov.in.": (
        "भारत सरकार के ओपन गवर्नमेंट डेटा प्लेटफ़ॉर्म data.gov.in से **{0}** ({1} ज़िला) के लिए **कर्नाटक** की लाइव मंडी कीमतें।",
        "ಭಾರತ ಸರ್ಕಾರದ ಓಪನ್ ಗವರ್ನಮೆಂಟ್ ಡೇಟಾ ವೇದಿಕೆ data.gov.in ನಿಂದ **{0}** ({1} ಜಿಲ್ಲೆ) ಗಾಗಿ **ಕರ್ನಾಟಕದ** ಲೈವ್ ಮಂಡಿ ಬೆಲೆಗಳು."),
    "data.gov.in API key": ("data.gov.in API कुंजी", "data.gov.in API ಕೀ"),
    "Enter your free data.gov.in API key to load live mandi prices.": (
        "लाइव मंडी भाव लोड करने के लिए अपनी निःशुल्क data.gov.in API कुंजी दर्ज करें।",
        "ಲೈವ್ ಮಂಡಿ ಬೆಲೆಗಳನ್ನು ಲೋಡ್ ಮಾಡಲು ನಿಮ್ಮ ಉಚಿತ data.gov.in API ಕೀ ನಮೂದಿಸಿ."),
    "Refresh": ("रीफ़्रेश", "ರಿಫ್ರೆಶ್"),
    "Enter your data.gov.in API key above to load live state mandi prices for {} ({} district). No sample or simulated prices are shown on this page.": (
        "{0} ({1} ज़िला) के लिए कर्नाटक की लाइव मंडी कीमतें लोड करने हेतु ऊपर अपनी data.gov.in API कुंजी दर्ज करें। इस पृष्ठ पर कोई नमूना या नकली कीमत नहीं दिखाई जाती।",
        "{0} ({1} ಜಿಲ್ಲೆ) ಗಾಗಿ ಕರ್ನಾಟಕದ ಲೈವ್ ಮಂಡಿ ಬೆಲೆಗಳನ್ನು ಲೋಡ್ ಮಾಡಲು ಮೇಲೆ ನಿಮ್ಮ data.gov.in API ಕೀ ನಮೂದಿಸಿ. ಈ ಪುಟದಲ್ಲಿ ಯಾವುದೇ ಮಾದರಿ ಅಥವಾ ಕೃತಕ ಬೆಲೆಗಳನ್ನು ತೋರಿಸಲಾಗುವುದಿಲ್ಲ."),
    "Loading state mandi prices for {}, {}...": (
        "{0}, {1} के लिए कर्नाटक की मंडी कीमतें लोड हो रही हैं...", "{0}, {1} ಗಾಗಿ ಕರ್ನಾಟಕ ಮಂಡಿ ಬೆಲೆಗಳನ್ನು ಲೋಡ್ ಮಾಡಲಾಗುತ್ತಿದೆ..."),
    "Showing {shown} of {total} crops, every vegetable priced individually, for <b>{location}</b>, {district} district • selected state/UT • prices in ₹ per quintal (100 kg)": (
        "<b>{location}</b>, {district} ज़िला • कर्नाटक के लिए {total} में से {shown} फसलें, हर सब्ज़ी का अलग भाव • कीमतें ₹ प्रति क्विंटल (100 किग्रा) में",
        "<b>{location}</b>, {district} ಜಿಲ್ಲೆ • ಕರ್ನಾಟಕಕ್ಕಾಗಿ {total} ಬೆಳೆಗಳಲ್ಲಿ {shown} ತೋರಿಸಲಾಗುತ್ತಿದೆ, ಪ್ರತಿ ತರಕಾರಿಗೂ ಪ್ರತ್ಯೇಕ ಬೆಲೆ • ಬೆಲೆಗಳು ₹ ಪ್ರತಿ ಕ್ವಿಂಟಲ್ (100 ಕೆ.ಜಿ.) ಗೆ"),
    "{} mandi": ("{0} मंडी", "{0} ಮಂಡಿ"),
    "{} district mandi": ("{0} ज़िला मंडी", "{0} ಜಿಲ್ಲಾ ಮಂಡಿ"),
    "State mandi": ("कर्नाटक की निकटतम मंडी", "ಕರ್ನಾಟಕದ ಹತ್ತಿರದ ಮಂಡಿ"),
    "Variety": ("किस्म", "ತಳಿ"),
    "Mandi": ("मंडी", "ಮಂಡಿ"),
    "Arrival date": ("आगमन तिथि", "ಆಗಮನ ದಿನಾಂಕ"),
    "/quintal": ("/क्विंटल", "/ಕ್ವಿಂಟಲ್"),
    "Min {}": ("न्यूनतम {0}", "ಕನಿಷ್ಠ {0}"),
    "Max {}": ("अधिकतम {0}", "ಗರಿಷ್ಠ {0}"),
    "No price reported today": ("आज कोई भाव दर्ज नहीं हुआ", "ಇಂದು ಯಾವುದೇ ಬೆಲೆ ವರದಿಯಾಗಿಲ್ಲ"),
    "No mandi price has been published for this crop in the latest available government update. Please check again later.": (
        "उपलब्ध नवीनतम सरकारी अपडेट में इस फसल के लिए कर्नाटक की कोई मंडी कीमत प्रकाशित नहीं हुई है। कृपया बाद में फिर देखें।",
        "ಲಭ್ಯವಿರುವ ಇತ್ತೀಚಿನ ಸರ್ಕಾರಿ ಅಪ್‌ಡೇಟ್‌ನಲ್ಲಿ ಈ ಬೆಳೆಗೆ ಕರ್ನಾಟಕದ ಯಾವುದೇ ಮಂಡಿ ಬೆಲೆ ಪ್ರಕಟವಾಗಿಲ್ಲ. ದಯವಿಟ್ಟು ನಂತರ ಮತ್ತೆ ಪರಿಶೀಲಿಸಿ."),
    "Source: Government of India • data.gov.in • Agmarknet daily mandi prices (Karnataka). Prices are the latest published records and may lag by a day or two. Verify at your local mandi before taking a financial decision.": (
        "स्रोत: भारत सरकार • data.gov.in • एगमार्कनेट दैनिक मंडी भाव (कर्नाटक)। कीमतें नवीनतम प्रकाशित रिकॉर्ड हैं और एक-दो दिन पीछे हो सकती हैं। वित्तीय निर्णय से पहले अपनी स्थानीय मंडी में पुष्टि करें।",
        "ಮೂಲ: ಭಾರತ ಸರ್ಕಾರ • data.gov.in • ಅಗ್ಮಾರ್ಕ್‌ನೆಟ್ ದೈನಂದಿನ ಮಂಡಿ ಬೆಲೆಗಳು (ಕರ್ನಾಟಕ). ಬೆಲೆಗಳು ಇತ್ತೀಚಿನ ಪ್ರಕಟಿತ ದಾಖಲೆಗಳಾಗಿದ್ದು ಒಂದು ಅಥವಾ ಎರಡು ದಿನ ವಿಳಂಬವಾಗಿರಬಹುದು. ಹಣಕಾಸು ನಿರ್ಧಾರಕ್ಕೂ ಮೊದಲು ನಿಮ್ಮ ಸ್ಥಳೀಯ ಮಂಡಿಯಲ್ಲಿ ಪರಿಶೀಲಿಸಿ."),
    "The data.gov.in service rejected this API key. Please check the key entered above, or generate a free key at data.gov.in.": (
        "data.gov.in सेवा ने इस API कुंजी को अस्वीकार कर दिया। कृपया ऊपर दर्ज कुंजी जाँचें या data.gov.in पर निःशुल्क कुंजी बनाएँ।",
        "data.gov.in ಸೇವೆಯು ಈ API ಕೀ ಅನ್ನು ತಿರಸ್ಕರಿಸಿದೆ. ದಯವಿಟ್ಟು ಮೇಲೆ ನಮೂದಿಸಿದ ಕೀ ಪರಿಶೀಲಿಸಿ ಅಥವಾ data.gov.in ನಲ್ಲಿ ಉಚಿತ ಕೀ ರಚಿಸಿ."),

    # ---- finance -------------------------------------------------------
    "Use these beginner-friendly calculators to plan business sales, evaluate loan EMIs, estimate affordability, and forecast monthly cash flows.": (
        "व्यवसाय बिक्री की योजना बनाने, ऋण EMI आँकने, वहनीयता का अनुमान लगाने और मासिक नकदी प्रवाह का पूर्वानुमान करने के लिए इन सरल कैलकुलेटरों का उपयोग करें।",
        "ವ್ಯವಹಾರ ಮಾರಾಟ ಯೋಜಿಸಲು, ಸಾಲದ EMI ಮೌಲ್ಯಮಾಪನ ಮಾಡಲು, ಕೈಗೆಟುಕುವಿಕೆ ಅಂದಾಜಿಸಲು ಮತ್ತು ಮಾಸಿಕ ನಗದು ಹರಿವು ಮುನ್ನಂದಾಜಿಸಲು ಈ ಸರಳ ಕ್ಯಾಲ್ಕುಲೇಟರ್‌ಗಳನ್ನು ಬಳಸಿ."),
    "Profit Margin": ("लाभ मार्जिन", "ಲಾಭ ಮಾರ್ಜಿನ್"),
    "Break-Even Analysis": ("ब्रेक-ईवन विश्लेषण", "ಬ್ರೇಕ್-ಈವನ್ ವಿಶ್ಲೇಷಣೆ"),
    "To cover your fixed/other costs of **{}**, you must sell at least **{} units** (total sales revenue of **{}**).": (
        "अपनी स्थिर/अन्य लागत **{0}** को पूरा करने के लिए आपको कम से कम **{1} इकाइयाँ** बेचनी होंगी (कुल बिक्री राजस्व **{2}**)।",
        "ನಿಮ್ಮ ಸ್ಥಿರ/ಇತರ ವೆಚ್ಚ **{0}** ಭರಿಸಲು ಕನಿಷ್ಠ **{1} ಘಟಕಗಳನ್ನು** ಮಾರಾಟ ಮಾಡಬೇಕು (ಒಟ್ಟು ಮಾರಾಟ ಆದಾಯ **{2}**)."),
    "Loan Affordability Calculator": ("ऋण वहनीयता कैलकुलेटर", "ಸಾಲ ಕೈಗೆಟುಕುವಿಕೆ ಕ್ಯಾಲ್ಕುಲೇಟರ್"),
    "Enter the principal amount you want to borrow and your monthly income details to see whether the estimated EMI fits your budget.": (
        "आप जो मूल राशि उधार लेना चाहते हैं और अपनी मासिक आय का विवरण दर्ज करें, ताकि देख सकें कि अनुमानित EMI आपके बजट में है या नहीं।",
        "ನೀವು ಸಾಲ ಪಡೆಯಲು ಬಯಸುವ ಮೂಲ ಮೊತ್ತ ಮತ್ತು ನಿಮ್ಮ ಮಾಸಿಕ ಆದಾಯದ ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ; ಅಂದಾಜು EMI ನಿಮ್ಮ ಬಜೆಟ್‌ಗೆ ಹೊಂದುತ್ತದೆಯೇ ಎಂದು ನೋಡಿ."),
    "Principal Amount / Loan Amount (₹)": ("मूल राशि / ऋण राशि (₹)", "ಮೂಲ ಮೊತ್ತ / ಸಾಲದ ಮೊತ್ತ (₹)"),
    "Monthly Income (₹)": ("मासिक आय (₹)", "ಮಾಸಿಕ ಆದಾಯ (₹)"),
    "Existing Monthly Living Expenses (₹)": ("मौजूदा मासिक जीवन-यापन खर्च (₹)", "ಈಗಿರುವ ಮಾಸಿಕ ಜೀವನ ವೆಚ್ಚಗಳು (₹)"),
    "Existing Monthly Loan EMIs (₹)": ("मौजूदा मासिक ऋण EMI (₹)", "ಈಗಿರುವ ಮಾಸಿಕ ಸಾಲ EMI ಗಳು (₹)"),
    "Proposed Loan Interest Rate (% p.a.)": ("प्रस्तावित ऋण ब्याज दर (% प्रति वर्ष)", "ಪ್ರಸ್ತಾವಿತ ಸಾಲದ ಬಡ್ಡಿ ದರ (% ವಾರ್ಷಿಕ)"),
    "Proposed Loan Period (Years)": ("प्रस्तावित ऋण अवधि (वर्ष)", "ಪ್ರಸ್ತಾವಿತ ಸಾಲದ ಅವಧಿ (ವರ್ಷಗಳು)"),
    "Principal Amount": ("मूल राशि", "ಮೂಲ ಮೊತ್ತ"),
    "Estimated EMI": ("अनुमानित EMI", "ಅಂದಾಜು EMI"),
    "Available Monthly Income": ("उपलब्ध मासिक आय", "ಲಭ್ಯವಿರುವ ಮಾಸಿಕ ಆದಾಯ"),
    "Total Interest": ("कुल ब्याज", "ಒಟ್ಟು ಬಡ್ಡಿ"),
    "The estimated EMI of **{}** is within your available monthly income of **{}** for the entered principal amount.": (
        "दर्ज मूल राशि के लिए अनुमानित EMI **{0}** आपकी उपलब्ध मासिक आय **{1}** के भीतर है।",
        "ನಮೂದಿಸಿದ ಮೂಲ ಮೊತ್ತಕ್ಕೆ ಅಂದಾಜು EMI **{0}** ನಿಮ್ಮ ಲಭ್ಯವಿರುವ ಮಾಸಿಕ ಆದಾಯ **{1}** ರ ಒಳಗಿದೆ."),
    "EMI uses the entered principal amount of **{}**, an interest rate of **{} p.a.**, and a loan period of **{} years**.": (
        "EMI की गणना दर्ज मूल राशि **{0}**, ब्याज दर **{1} प्रति वर्ष** और ऋण अवधि **{2} वर्ष** से की गई है।",
        "EMI ಅನ್ನು ನಮೂದಿಸಿದ ಮೂಲ ಮೊತ್ತ **{0}**, ಬಡ್ಡಿ ದರ **{1} ವಾರ್ಷಿಕ** ಮತ್ತು ಸಾಲದ ಅವಧಿ **{2} ವರ್ಷಗಳು** ಆಧರಿಸಿ ಲೆಕ್ಕಿಸಲಾಗಿದೆ."),
    "This is a simple planning estimate. Actual loan eligibility, interest rates, fees and repayment terms depend on the lender.": (
        "यह एक सरल योजना अनुमान है। वास्तविक ऋण पात्रता, ब्याज दर, शुल्क और चुकौती शर्तें ऋणदाता पर निर्भर करती हैं।",
        "ಇದು ಸರಳ ಯೋಜನಾ ಅಂದಾಜು. ನಿಜವಾದ ಸಾಲ ಅರ್ಹತೆ, ಬಡ್ಡಿ ದರ, ಶುಲ್ಕ ಮತ್ತು ಮರುಪಾವತಿ ನಿಯಮಗಳು ಸಾಲದಾತರ ಮೇಲೆ ಅವಲಂಬಿತವಾಗಿವೆ."),
    "Loan Affordability": ("ऋण वहनीयता", "ಸಾಲ ಕೈಗೆಟುಕುವಿಕೆ"),
    "Monthly Cash Flow Planner": ("मासिक नकदी प्रवाह योजनाकार", "ಮಾಸಿಕ ನಗದು ಹರಿವು ಯೋಜಕ"),
    "Plan your expected monthly income and expenses to estimate your remaining cash flow.": (
        "अपनी अपेक्षित मासिक आय और खर्च की योजना बनाकर शेष नकदी प्रवाह का अनुमान लगाएँ।",
        "ನಿಮ್ಮ ನಿರೀಕ್ಷಿತ ಮಾಸಿಕ ಆದಾಯ ಮತ್ತು ವೆಚ್ಚಗಳನ್ನು ಯೋಜಿಸಿ ಉಳಿಯುವ ನಗದು ಹರಿವನ್ನು ಅಂದಾಜಿಸಿ."),
    "Expected Monthly Business/Family Income (₹)": ("अपेक्षित मासिक व्यवसाय/पारिवारिक आय (₹)", "ನಿರೀಕ್ಷಿತ ಮಾಸಿಕ ವ್ಯವಹಾರ/ಕುಟುಂಬ ಆದಾಯ (₹)"),
    "Monthly Operating / Business Expenses (₹)": ("मासिक संचालन / व्यवसाय खर्च (₹)", "ಮಾಸಿಕ ಕಾರ್ಯಾಚರಣಾ / ವ್ಯವಹಾರ ವೆಚ್ಚಗಳು (₹)"),
    "Monthly Household / Personal Expenses (₹)": ("मासिक घरेलू / व्यक्तिगत खर्च (₹)", "ಮಾಸಿಕ ಮನೆ / ವೈಯಕ್ತಿಕ ವೆಚ್ಚಗಳು (₹)"),
    "Total Monthly Debt / EMI Payments (₹)": ("कुल मासिक ऋण / EMI भुगतान (₹)", "ಒಟ್ಟು ಮಾಸಿಕ ಸಾಲ / EMI ಪಾವತಿಗಳು (₹)"),
    "Total Monthly Income": ("कुल मासिक आय", "ಒಟ್ಟು ಮಾಸಿಕ ಆದಾಯ"),
    "Total Monthly Expenses": ("कुल मासिक खर्च", "ಒಟ್ಟು ಮಾಸಿಕ ವೆಚ್ಚಗಳು"),
    "Remaining Cash Flow": ("शेष नकदी प्रवाह", "ಉಳಿಯುವ ನಗದು ಹರಿವು"),
    "Positive Cash Flow": ("सकारात्मक नकदी प्रवाह", "ಧನಾತ್ಮಕ ನಗದು ಹರಿವು"),
    "{} remains after the entered monthly expenses and EMIs.": (
        "दर्ज मासिक खर्च और EMI के बाद {0} शेष रहता है।", "ನಮೂದಿಸಿದ ಮಾಸಿಕ ವೆಚ್ಚಗಳು ಮತ್ತು EMI ಗಳ ನಂತರ {0} ಉಳಿಯುತ್ತದೆ."),
    "Financial Safety Note": ("वित्तीय सुरक्षा नोट", "ಹಣಕಾಸು ಸುರಕ್ಷತಾ ಟಿಪ್ಪಣಿ"),
    "All calculations provided in this section are estimates for guidance and educational planning. Actual bank interest rates, repayment schedules, and loan eligibility decisions depend on official lender policies.": (
        "इस भाग की सभी गणनाएँ मार्गदर्शन और शैक्षिक योजना के लिए अनुमान हैं। वास्तविक बैंक ब्याज दरें, चुकौती कार्यक्रम और ऋण पात्रता के निर्णय ऋणदाता की आधिकारिक नीतियों पर निर्भर करते हैं।",
        "ಈ ವಿಭಾಗದ ಎಲ್ಲಾ ಲೆಕ್ಕಾಚಾರಗಳು ಮಾರ್ಗದರ್ಶನ ಮತ್ತು ಶೈಕ್ಷಣಿಕ ಯೋಜನೆಗಾಗಿ ಮಾಡಿದ ಅಂದಾಜುಗಳು. ನಿಜವಾದ ಬ್ಯಾಂಕ್ ಬಡ್ಡಿ ದರಗಳು, ಮರುಪಾವತಿ ವೇಳಾಪಟ್ಟಿ ಮತ್ತು ಸಾಲ ಅರ್ಹತೆ ನಿರ್ಧಾರಗಳು ಸಾಲದಾತರ ಅಧಿಕೃತ ನೀತಿಗಳ ಮೇಲೆ ಅವಲಂಬಿತವಾಗಿವೆ."),

    # ---- schemes page --------------------------------------------------
    "GRAM SAHAYAK • SCHEME DISCOVERY": ("ग्राम सहायक • योजना खोज", "ಗ್ರಾಮ ಸಹಾಯಕ • ಯೋಜನೆ ಅನ್ವೇಷಣೆ"),
    "User / Beneficiary Type": ("उपयोगकर्ता / लाभार्थी प्रकार", "ಬಳಕೆದಾರ / ಫಲಾನುಭವಿ ಪ್ರಕಾರ"),
    "Business Stage": ("व्यवसाय चरण", "ವ್ಯವಹಾರ ಹಂತ"),
    "Activity Category": ("गतिविधि श्रेणी", "ಚಟುವಟಿಕೆ ವರ್ಗ"),
    "Approximate Funding Requirement (₹)": ("अनुमानित धन आवश्यकता (₹)", "ಅಂದಾಜು ಹಣಕಾಸು ಅಗತ್ಯ (₹)"),
    "Show matches only (>30% profile match)": ("केवल मिलान दिखाएँ (>30% प्रोफ़ाइल मिलान)", "ಹೊಂದಾಣಿಕೆಗಳನ್ನು ಮಾತ್ರ ತೋರಿಸಿ (>30% ಪ್ರೊಫೈಲ್ ಹೊಂದಾಣಿಕೆ)"),
    "Schemes shown": ("दिखाई गई योजनाएँ", "ತೋರಿಸಿದ ಯೋಜನೆಗಳು"),
    "Profile matches": ("प्रोफ़ाइल मिलान", "ಪ್ರೊಫೈಲ್ ಹೊಂದಾಣಿಕೆಗಳು"),
    "Funding range fit": ("धन सीमा अनुकूलता", "ಹಣಕಾಸು ಮಿತಿ ಹೊಂದಾಣಿಕೆ"),
    "Total schemes": ("कुल योजनाएँ", "ಒಟ್ಟು ಯೋಜನೆಗಳು"),
    "Matches are calculated programmatically for profile alignment. This is NOT an official eligibility confirmation.": (
        "मिलान प्रोफ़ाइल अनुरूपता के लिए प्रोग्राम द्वारा गणना किए जाते हैं। यह आधिकारिक पात्रता की पुष्टि नहीं है।",
        "ಹೊಂದಾಣಿಕೆಗಳನ್ನು ಪ್ರೊಫೈಲ್ ಸರಿಹೊಂದಿಕೆಗಾಗಿ ಪ್ರೋಗ್ರಾಂ ಮೂಲಕ ಲೆಕ್ಕಿಸಲಾಗುತ್ತದೆ. ಇದು ಅಧಿಕೃತ ಅರ್ಹತೆಯ ದೃಢೀಕರಣವಲ್ಲ."),
    "{} Profile Match": ("{0} प्रोफ़ाइल मिलान", "{0} ಪ್ರೊಫೈಲ್ ಹೊಂದಾಣಿಕೆ"),
    "Key Benefit": ("मुख्य लाभ", "ಪ್ರಮುಖ ಲಾಭ"),
    "Purpose & Description": ("उद्देश्य और विवरण", "ಉದ್ದೇಶ ಮತ್ತು ವಿವರಣೆ"),
    "Target Beneficiaries": ("लक्षित लाभार्थी", "ಗುರಿ ಫಲಾನುಭವಿಗಳು"),
    "Financial Support / Range": ("वित्तीय सहायता / सीमा", "ಹಣಕಾಸು ಬೆಂಬಲ / ಮಿತಿ"),
    "Major Eligibility Conditions": ("प्रमुख पात्रता शर्तें", "ಪ್ರಮುಖ ಅರ್ಹತಾ ಷರತ್ತುಗಳು"),
    "Important Documents Required": ("आवश्यक महत्वपूर्ण दस्तावेज़", "ಅಗತ್ಯವಿರುವ ಪ್ರಮುಖ ದಾಖಲೆಗಳು"),
    "Official Source / Portal": ("आधिकारिक स्रोत / पोर्टल", "ಅಧಿಕೃತ ಮೂಲ / ಪೋರ್ಟಲ್"),
    "Why this matches": ("यह क्यों मेल खाता है", "ಇದು ಏಕೆ ಹೊಂದಾಣಿಕೆಯಾಗುತ್ತದೆ"),
    "Why this scheme may be relevant": ("यह योजना क्यों प्रासंगिक हो सकती है", "ಈ ಯೋಜನೆ ಏಕೆ ಪ್ರಸ್ತುತವಾಗಿರಬಹುದು"),
    "Profile alignment": ("प्रोफ़ाइल अनुरूपता", "ಪ್ರೊಫೈಲ್ ಸರಿಹೊಂದಿಕೆ"),
    "Visit Official Website": ("आधिकारिक वेबसाइट पर जाएँ", "ಅಧಿಕೃತ ವೆಬ್‌ಸೈಟ್‌ಗೆ ಭೇಟಿ ನೀಡಿ"),
    "Open Official Portal": ("आधिकारिक पोर्टल खोलें", "ಅಧಿಕೃತ ಪೋರ್ಟಲ್ ತೆರೆಯಿರಿ"),
    "View scheme details": ("योजना विवरण देखें", "ಯೋಜನೆಯ ವಿವರಗಳನ್ನು ನೋಡಿ"),
    "Funding requirement ({}) falls within the scheme range.": (
        "धन आवश्यकता ({0}) योजना की सीमा के भीतर है।", "ಹಣಕಾಸು ಅಗತ್ಯ ({0}) ಯೋಜನೆಯ ಮಿತಿಯೊಳಗೆ ಇದೆ."),
    "Funding requirement is outside the indicative range ({} – {}).": (
        "धन आवश्यकता सांकेतिक सीमा ({0} – {1}) से बाहर है।", "ಹಣಕಾಸು ಅಗತ್ಯ ಸೂಚಕ ಮಿತಿ ({0} – {1}) ಹೊರಗಿದೆ."),
    "Indicative range: {} – {}": ("सांकेतिक सीमा: {0} – {1}", "ಸೂಚಕ ಮಿತಿ: {0} – {1}"),
    "Funding amount is determined by the applicable scheme component, lender or current guidelines.": (
        "धन राशि लागू योजना घटक, ऋणदाता या वर्तमान दिशानिर्देशों से तय होती है।",
        "ಹಣದ ಮೊತ್ತವನ್ನು ಅನ್ವಯಿಸುವ ಯೋಜನಾ ಘಟಕ, ಸಾಲದಾತ ಅಥವಾ ಪ್ರಸ್ತುತ ಮಾರ್ಗಸೂಚಿಗಳು ನಿರ್ಧರಿಸುತ್ತವೆ."),
    "Relevant when the applicant/business matches the scheme's stated beneficiary type, stage and activity conditions.": (
        "तब प्रासंगिक जब आवेदक/व्यवसाय योजना में बताए गए लाभार्थी प्रकार, चरण और गतिविधि शर्तों से मेल खाता हो।",
        "ಅರ್ಜಿದಾರ/ವ್ಯವಹಾರವು ಯೋಜನೆಯಲ್ಲಿ ಹೇಳಿದ ಫಲಾನುಭವಿ ಪ್ರಕಾರ, ಹಂತ ಮತ್ತು ಚಟುವಟಿಕೆ ಷರತ್ತುಗಳಿಗೆ ಹೊಂದಿದಾಗ ಪ್ರಸ್ತುತ."),
    "All": ("सभी", "ಎಲ್ಲಾ"),

    # ---- business page -------------------------------------------------
    "1️⃣ Step 1 — Select Business": ("1️⃣ चरण 1 — व्यवसाय चुनें", "1️⃣ ಹಂತ 1 — ವ್ಯವಹಾರ ಆಯ್ಕೆಮಾಡಿ"),
    "2️⃣ Step 2 — Enter Inputs": ("2️⃣ चरण 2 — जानकारी भरें", "2️⃣ ಹಂತ 2 — ಮಾಹಿತಿ ನಮೂದಿಸಿ"),
    "3️⃣ Step 3 — Strategic Output": ("3️⃣ चरण 3 — रणनीतिक परिणाम", "3️⃣ ಹಂತ 3 — ತಂತ್ರಾತ್ಮಕ ಫಲಿತಾಂಶ"),
    "Complete Step 1, then Step 2. Step 3 appears only after recommendations are generated and lets you select an activity for its strategic guidance and related schemes.": (
        "पहले चरण 1, फिर चरण 2 पूरा करें। चरण 3 सुझाव बनने के बाद ही दिखता है और आपको रणनीतिक मार्गदर्शन व संबंधित योजनाओं के लिए गतिविधि चुनने देता है।",
        "ಮೊದಲು ಹಂತ 1, ನಂತರ ಹಂತ 2 ಪೂರ್ಣಗೊಳಿಸಿ. ಶಿಫಾರಸುಗಳು ರಚನೆಯಾದ ನಂತರ ಮಾತ್ರ ಹಂತ 3 ಕಾಣಿಸುತ್ತದೆ; ಅದರ ತಂತ್ರಾತ್ಮಕ ಮಾರ್ಗದರ್ಶನ ಮತ್ತು ಸಂಬಂಧಿತ ಯೋಜನೆಗಳಿಗಾಗಿ ಚಟುವಟಿಕೆ ಆರಿಸಬಹುದು."),
    "Choose the business domain and activity first. The selected location is reused automatically throughout this assessment.": (
        "पहले व्यवसाय क्षेत्र और गतिविधि चुनें। चुना गया स्थान इस पूरे आकलन में अपने-आप उपयोग होता है।",
        "ಮೊದಲು ವ್ಯವಹಾರ ಕ್ಷೇತ್ರ ಮತ್ತು ಚಟುವಟಿಕೆಯನ್ನು ಆರಿಸಿ. ಆಯ್ಕೆ ಮಾಡಿದ ಸ್ಥಳವು ಈ ಮೌಲ್ಯಮಾಪನದುದ್ದಕ್ಕೂ ತಾನಾಗಿ ಬಳಕೆಯಾಗುತ್ತದೆ."),
    "Business Domain": ("व्यवसाय क्षेत्र", "ವ್ಯವಹಾರ ಕ್ಷೇತ್ರ"),
    "Business Activity": ("व्यवसाय गतिविधि", "ವ್ಯವಹಾರ ಚಟುವಟಿಕೆ"),
    "Used automatically for this assessment": ("इस आकलन के लिए अपने-आप उपयोग", "ಈ ಮೌಲ್ಯಮಾಪನಕ್ಕೆ ತಾನಾಗಿ ಬಳಕೆ"),
    "Numeric inputs start at 0 and text inputs start blank. Water and temperature are taken automatically from the selected location.": (
        "संख्यात्मक इनपुट 0 से और पाठ इनपुट खाली से शुरू होते हैं। पानी और तापमान चुने गए स्थान से अपने-आप लिए जाते हैं।",
        "ಸಂಖ್ಯಾ ಇನ್‌ಪುಟ್‌ಗಳು 0 ಯಿಂದ ಮತ್ತು ಪಠ್ಯ ಇನ್‌ಪುಟ್‌ಗಳು ಖಾಲಿಯಿಂದ ಪ್ರಾರಂಭವಾಗುತ್ತವೆ. ನೀರು ಮತ್ತು ತಾಪಮಾನವನ್ನು ಆಯ್ಕೆ ಮಾಡಿದ ಸ್ಥಳದಿಂದ ತಾನಾಗಿ ತೆಗೆದುಕೊಳ್ಳಲಾಗುತ್ತದೆ."),
    "Water availability": ("पानी की उपलब्धता", "ನೀರಿನ ಲಭ್ಯತೆ"),
    "Irrigation baseline": ("सिंचाई आधार स्तर", "ನೀರಾವರಿ ಮೂಲ ಮಟ್ಟ"),
    "Location temperature": ("स्थान का तापमान", "ಸ್ಥಳದ ತಾಪಮಾನ"),
    "Rainfall": ("वर्षा", "ಮಳೆ"),
    "Temperature source": ("तापमान स्रोत", "ತಾಪಮಾನದ ಮೂಲ"),
    "Location planning profile": ("स्थान योजना प्रोफ़ाइल", "ಸ್ಥಳ ಯೋಜನಾ ಪ್ರೊಫೈಲ್"),
    "Location temperature: **{} °C** · Location planning profile": (
        "स्थान का तापमान: **{0} °C** · स्थान योजना प्रोफ़ाइल", "ಸ್ಥಳದ ತಾಪಮಾನ: **{0} °C** · ಸ್ಥಳ ಯೋಜನಾ ಪ್ರೊಫೈಲ್"),
    "The temperature field is automatic and cannot be manually overridden.": (
        "तापमान फ़ील्ड स्वचालित है और हाथ से बदला नहीं जा सकता।", "ತಾಪಮಾನ ಕ್ಷೇತ್ರ ಸ್ವಯಂಚಾಲಿತವಾಗಿದ್ದು ಕೈಯಾರೆ ಬದಲಾಯಿಸಲು ಸಾಧ್ಯವಿಲ್ಲ."),
    "Species / Variety / Product Selection": ("प्रजाति / किस्म / उत्पाद चयन", "ಜಾತಿ / ತಳಿ / ಉತ್ಪನ್ನ ಆಯ್ಕೆ"),
    "Location & Climate Parameters": ("स्थान और जलवायु पैरामीटर", "ಸ್ಥಳ ಮತ್ತು ಹವಾಮಾನ ನಿಯತಾಂಕಗಳು"),
    "Soil & Water Profile": ("मिट्टी और पानी प्रोफ़ाइल", "ಮಣ್ಣು ಮತ್ತು ನೀರಿನ ಪ್ರೊಫೈಲ್"),
    "Capital & Financial Goals": ("पूंजी और वित्तीय लक्ष्य", "ಬಂಡವಾಳ ಮತ್ತು ಹಣಕಾಸು ಗುರಿಗಳು"),
    "Generate Business Recommendations": ("व्यवसाय सुझाव बनाएँ", "ವ್ಯವಹಾರ ಶಿಫಾರಸುಗಳನ್ನು ರಚಿಸಿ"),
    "Step 3 — Strategic Output": ("चरण 3 — रणनीतिक परिणाम", "ಹಂತ 3 — ತಂತ್ರಾತ್ಮಕ ಫಲಿತಾಂಶ"),
    "Select the generated activity you want. Execution, advisory, risks, financial guidance and related schemes appear below.": (
        "बनाई गई गतिविधियों में से अपनी पसंद चुनें। कार्यान्वयन, सलाह, जोखिम, वित्तीय मार्गदर्शन और संबंधित योजनाएँ नीचे दिखती हैं।",
        "ರಚಿಸಿದ ಚಟುವಟಿಕೆಗಳಲ್ಲಿ ನಿಮಗೆ ಬೇಕಾದದ್ದನ್ನು ಆರಿಸಿ. ಕಾರ್ಯಗತಗೊಳಿಸುವಿಕೆ, ಸಲಹೆ, ಅಪಾಯಗಳು, ಹಣಕಾಸು ಮಾರ್ಗದರ್ಶನ ಮತ್ತು ಸಂಬಂಧಿತ ಯೋಜನೆಗಳು ಕೆಳಗೆ ಕಾಣಿಸುತ್ತವೆ."),
    "Select your preferred business option": ("अपना पसंदीदा व्यवसाय विकल्प चुनें", "ನಿಮ್ಮ ಆದ್ಯತೆಯ ವ್ಯವಹಾರ ಆಯ್ಕೆಯನ್ನು ಆರಿಸಿ"),
    "Environmental crop check": ("पर्यावरणीय फसल जाँच", "ಪರಿಸರ ಬೆಳೆ ಪರಿಶೀಲನೆ"),
    "Reference check": ("संदर्भ जाँच", "ಉಲ್ಲೇಖ ಪರಿಶೀಲನೆ"),
    "Score": ("स्कोर", "ಅಂಕ"),
    "Reason": ("कारण", "ಕಾರಣ"),
    "Pass": ("सफल", "ಪಾಸ್"),
    "Check": ("जाँचें", "ಪರಿಶೀಲಿಸಿ"),
    "Not selected": ("चुना नहीं गया", "ಆಯ್ಕೆ ಮಾಡಿಲ್ಲ"),
    "Agriculture checks / advisory notes": ("कृषि जाँच / सलाह नोट", "ಕೃಷಿ ಪರಿಶೀಲನೆ / ಸಲಹಾ ಟಿಪ್ಪಣಿಗಳು"),
    "needs attention before starting": ("शुरू करने से पहले ध्यान देने की आवश्यकता", "ಪ್ರಾರಂಭಿಸುವ ಮೊದಲು ಗಮನ ಬೇಕು"),
    "Missing or unknown inputs not used in the score": (
        "अनुपलब्ध या अज्ञात इनपुट स्कोर में उपयोग नहीं किए गए", "ಕಾಣೆಯಾದ ಅಥವಾ ಅಜ್ಞಾತ ಇನ್‌ಪುಟ್‌ಗಳನ್ನು ಅಂಕದಲ್ಲಿ ಬಳಸಿಲ್ಲ"),
    "Rule-based fit score from currently available inputs.": (
        "वर्तमान उपलब्ध इनपुट से नियम-आधारित उपयुक्तता स्कोर।", "ಪ್ರಸ್ತುತ ಲಭ್ಯವಿರುವ ಇನ್‌ಪುಟ್‌ಗಳಿಂದ ನಿಯಮಾಧಾರಿತ ಹೊಂದಾಣಿಕೆ ಅಂಕ."),
    "Indicative model output, not guaranteed income.": ("सांकेतिक मॉडल परिणाम, गारंटीशुदा आय नहीं।", "ಸೂಚಕ ಮಾದರಿ ಫಲಿತಾಂಶ, ಖಾತರಿಯ ಆದಾಯವಲ್ಲ."),
    "Prototype planning range; validate supplier/asset quotes.": (
        "प्रोटोटाइप योजना सीमा; आपूर्तिकर्ता/संपत्ति के भाव सत्यापित करें।", "ಪ್ರೋಟೋಟೈಪ್ ಯೋಜನಾ ಮಿತಿ; ಪೂರೈಕೆದಾರ/ಸ್ವತ್ತಿನ ದರಗಳನ್ನು ಪರಿಶೀಲಿಸಿ."),
    "Scale-dependent estimate.": ("पैमाने पर निर्भर अनुमान।", "ಪ್ರಮಾಣವನ್ನು ಅವಲಂಬಿಸಿದ ಅಂದಾಜು."),
    "Based on the current input or configured recommendation.": (
        "वर्तमान इनपुट या कॉन्फ़िगर की गई सिफारिश पर आधारित।", "ಪ್ರಸ್ತುತ ಇನ್‌ಪುಟ್ ಅಥವಾ ಕಾನ್ಫಿಗರ್ ಮಾಡಿದ ಶಿಫಾರಸಿನ ಆಧಾರದ ಮೇಲೆ."),
    "Depends on realized contribution margin and sales/production volume.": (
        "प्राप्त योगदान मार्जिन और बिक्री/उत्पादन मात्रा पर निर्भर।", "ಗಳಿಸಿದ ಕೊಡುಗೆ ಮಾರ್ಜಿನ್ ಮತ್ತು ಮಾರಾಟ/ಉತ್ಪಾದನಾ ಪ್ರಮಾಣವನ್ನು ಅವಲಂಬಿಸಿದೆ."),
    "Close this gap or test a smaller pilot before scaling.": (
        "विस्तार से पहले इस कमी को दूर करें या छोटा पायलट परीक्षण करें।", "ವಿಸ್ತರಿಸುವ ಮೊದಲು ಈ ಅಂತರವನ್ನು ಮುಚ್ಚಿ ಅಥವಾ ಸಣ್ಣ ಪೈಲಟ್ ಪರೀಕ್ಷಿಸಿ."),
    "Prepare → pilot → validate → scale. Each phase has a clear outcome and a go/no-go gate.": (
        "तैयारी → पायलट → सत्यापन → विस्तार। हर चरण का स्पष्ट परिणाम और आगे बढ़ने/रुकने का द्वार है।",
        "ಸಿದ್ಧತೆ → ಪೈಲಟ್ → ಪರಿಶೀಲನೆ → ವಿಸ್ತರಣೆ. ಪ್ರತಿ ಹಂತಕ್ಕೂ ಸ್ಪಷ್ಟ ಫಲಿತಾಂಶ ಮತ್ತು ಮುಂದುವರಿಯುವ/ನಿಲ್ಲಿಸುವ ಗೇಟ್ ಇದೆ."),
    "Gate 1 · Site + resources + budget confirmed": ("गेट 1 · स्थान + संसाधन + बजट पुष्ट", "ಗೇಟ್ 1 · ಸ್ಥಳ + ಸಂಪನ್ಮೂಲ + ಬಜೆಟ್ ದೃಢ"),
    "Gate 2 · Pilot data meets the planned operating thresholds": (
        "गेट 2 · पायलट डेटा नियोजित संचालन सीमाओं को पूरा करता है", "ಗೇಟ್ 2 · ಪೈಲಟ್ ಡೇಟಾ ಯೋಜಿತ ಕಾರ್ಯಾಚರಣಾ ಮಿತಿಗಳನ್ನು ಪೂರೈಸುತ್ತದೆ"),
    "Gate 3 · Repeat demand + workable unit economics + operational control": (
        "गेट 3 · दोहराई मांग + व्यवहार्य इकाई अर्थशास्त्र + संचालन नियंत्रण", "ಗೇಟ್ 3 · ಪುನರಾವರ್ತಿತ ಬೇಡಿಕೆ + ಕಾರ್ಯಸಾಧ್ಯ ಘಟಕ ಅರ್ಥಶಾಸ್ತ್ರ + ಕಾರ್ಯಾಚರಣಾ ನಿಯಂತ್ರಣ"),
    "No business-specific selection library is configured for this activity yet.": (
        "इस गतिविधि के लिए अभी कोई व्यवसाय-विशिष्ट चयन सूची कॉन्फ़िगर नहीं है।", "ಈ ಚಟುವಟಿಕೆಗೆ ಇನ್ನೂ ವ್ಯವಹಾರ-ನಿರ್ದಿಷ್ಟ ಆಯ್ಕೆ ಪಟ್ಟಿ ಕಾನ್ಫಿಗರ್ ಆಗಿಲ್ಲ."),
    "Environmental reference dataset unavailable": ("पर्यावरणीय संदर्भ डेटासेट उपलब्ध नहीं", "ಪರಿಸರ ಉಲ್ಲೇಖ ಡೇಟಾಸೆಟ್ ಲಭ್ಯವಿಲ್ಲ"),
    "The NPK reference CSV is not available in this deployment, so environmental matching is limited to the location profile.": (
        "इस परिनियोजन में NPK संदर्भ CSV उपलब्ध नहीं है, इसलिए पर्यावरणीय मिलान केवल स्थान प्रोफ़ाइल तक सीमित है।",
        "ಈ ನಿಯೋಜನೆಯಲ್ಲಿ NPK ಉಲ್ಲೇಖ CSV ಲಭ್ಯವಿಲ್ಲ, ಆದ್ದರಿಂದ ಪರಿಸರ ಹೊಂದಾಣಿಕೆ ಸ್ಥಳ ಪ್ರೊಫೈಲ್‌ಗೆ ಸೀಮಿತವಾಗಿದೆ."),
    "Showing {} of {} location-suitable options in this dashboard. The full location mapping remains the source list.": (
        "इस डैशबोर्ड में {1} में से {0} स्थान-उपयुक्त विकल्प दिखाए जा रहे हैं। पूर्ण स्थान मैपिंग ही स्रोत सूची है।",
        "ಈ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ನಲ್ಲಿ {1} ಸ್ಥಳ-ಸೂಕ್ತ ಆಯ್ಕೆಗಳಲ್ಲಿ {0} ತೋರಿಸಲಾಗುತ್ತಿದೆ. ಪೂರ್ಣ ಸ್ಥಳ ಮ್ಯಾಪಿಂಗ್ ಮೂಲ ಪಟ್ಟಿಯಾಗಿಯೇ ಉಳಿಯುತ್ತದೆ."),
    "Location filter: {}. The candidate list comes from the prototype's location-to-crop mapping; feasibility is then assessed from the inputs you supplied.": (
        "स्थान फ़िल्टर: {0}। उम्मीदवार सूची प्रोटोटाइप के स्थान-से-फसल मैपिंग से आती है; फिर आपके दिए इनपुट से व्यवहार्यता आँकी जाती है।",
        "ಸ್ಥಳ ಫಿಲ್ಟರ್: {0}. ಅಭ್ಯರ್ಥಿ ಪಟ್ಟಿ ಪ್ರೋಟೋಟೈಪ್‌ನ ಸ್ಥಳ-ಬೆಳೆ ಮ್ಯಾಪಿಂಗ್‌ನಿಂದ ಬರುತ್ತದೆ; ನಂತರ ನೀವು ನೀಡಿದ ಇನ್‌ಪುಟ್‌ಗಳಿಂದ ಕಾರ್ಯಸಾಧ್ಯತೆ ಮೌಲ್ಯಮಾಪನವಾಗುತ್ತದೆ."),
    "Land area has not been entered yet.": ("भूमि क्षेत्र अभी दर्ज नहीं किया गया है।", "ಭೂಮಿ ವಿಸ್ತೀರ್ಣವನ್ನು ಇನ್ನೂ ನಮೂದಿಸಿಲ್ಲ."),
    "Available investment has not been entered yet.": ("उपलब्ध निवेश अभी दर्ज नहीं किया गया है।", "ಲಭ್ಯವಿರುವ ಹೂಡಿಕೆಯನ್ನು ಇನ್ನೂ ನಮೂದಿಸಿಲ್ಲ."),
    "Market access is set to Poor; confirm at least two buyers before scaling.": (
        "बाज़ार पहुँच 'कमज़ोर' है; विस्तार से पहले कम से कम दो खरीदारों की पुष्टि करें।", "ಮಾರುಕಟ್ಟೆ ಪ್ರವೇಶ 'ದುರ್ಬಲ' ಎಂದಿದೆ; ವಿಸ್ತರಿಸುವ ಮೊದಲು ಕನಿಷ್ಠ ಇಬ್ಬರು ಖರೀದಿದಾರರನ್ನು ದೃಢಪಡಿಸಿ."),
    "At least one reliable labour resource should be planned for routine field operations.": (
        "नियमित खेत कार्यों के लिए कम से कम एक भरोसेमंद श्रमिक की योजना बनाएँ।", "ನಿತ್ಯದ ಹೊಲ ಕೆಲಸಗಳಿಗೆ ಕನಿಷ್ಠ ಒಬ್ಬ ವಿಶ್ವಾಸಾರ್ಹ ಕಾರ್ಮಿಕರನ್ನು ಯೋಜಿಸಬೇಕು."),
    "Consider the reliability of the electricity connection at the operating site.": (
        "संचालन स्थल पर बिजली कनेक्शन की विश्वसनीयता पर विचार करें।", "ಕಾರ್ಯಾಚರಣಾ ಸ್ಥಳದಲ್ಲಿ ವಿದ್ಯುತ್ ಸಂಪರ್ಕದ ವಿಶ್ವಾಸಾರ್ಹತೆಯನ್ನು ಪರಿಗಣಿಸಿ."),
    "Use a recent water-quality test where available.": (
        "जहाँ उपलब्ध हो, हाल की जल-गुणवत्ता जाँच का उपयोग करें।", "ಲಭ್ಯವಿದ್ದಲ್ಲಿ ಇತ್ತೀಚಿನ ನೀರಿನ ಗುಣಮಟ್ಟ ಪರೀಕ್ಷೆಯನ್ನು ಬಳಸಿ."),
    "Estimate current local demand from farmers or service buyers.": (
        "किसानों या सेवा खरीदारों से वर्तमान स्थानीय मांग का अनुमान लगाएँ।", "ರೈತರು ಅಥವಾ ಸೇವಾ ಖರೀದಿದಾರರಿಂದ ಪ್ರಸ್ತುತ ಸ್ಥಳೀಯ ಬೇಡಿಕೆಯನ್ನು ಅಂದಾಜಿಸಿ."),
    "Rate the practical access you have to buyers after transport and handling.": (
        "परिवहन और हैंडलिंग के बाद खरीदारों तक अपनी व्यावहारिक पहुँच का आकलन करें।", "ಸಾರಿಗೆ ಮತ್ತು ನಿರ್ವಹಣೆಯ ನಂತರ ಖರೀದಿದಾರರಿಗೆ ನಿಮ್ಮ ಪ್ರಾಯೋಗಿಕ ಪ್ರವೇಶವನ್ನು ರೇಟ್ ಮಾಡಿ."),
    "Choose the crop, animal type, fish species, nursery plant, processed product or service type you plan to work with.": (
        "जिस फसल, पशु प्रकार, मछली प्रजाति, नर्सरी पौधे, प्रसंस्कृत उत्पाद या सेवा प्रकार पर काम करना चाहते हैं, उसे चुनें।",
        "ನೀವು ಕೆಲಸ ಮಾಡಲು ಯೋಜಿಸಿರುವ ಬೆಳೆ, ಪ್ರಾಣಿ ಪ್ರಕಾರ, ಮೀನು ಜಾತಿ, ನರ್ಸರಿ ಸಸ್ಯ, ಸಂಸ್ಕರಿತ ಉತ್ಪನ್ನ ಅಥವಾ ಸೇವಾ ಪ್ರಕಾರವನ್ನು ಆರಿಸಿ."),
    "Choose the intended production season.": ("इच्छित उत्पादन मौसम चुनें।", "ಉದ್ದೇಶಿತ ಉತ್ಪಾದನಾ ಋತುವನ್ನು ಆರಿಸಿ."),
    "Choose the experience level you can rely on for this activity.": (
        "इस गतिविधि के लिए जिस अनुभव स्तर पर आप भरोसा कर सकते हैं, उसे चुनें।", "ಈ ಚಟುವಟಿಕೆಗೆ ನೀವು ಅವಲಂಬಿಸಬಹುದಾದ ಅನುಭವ ಮಟ್ಟವನ್ನು ಆರಿಸಿ."),
    "Choose the time window in which you need the activity to start generating income.": (
        "वह समय-सीमा चुनें जिसमें आपको गतिविधि से आय शुरू होनी चाहिए।", "ಚಟುವಟಿಕೆಯಿಂದ ಆದಾಯ ಪ್ರಾರಂಭವಾಗಬೇಕಾದ ಕಾಲಾವಧಿಯನ್ನು ಆರಿಸಿ."),
    "Enter only capital you can actually deploy for this business.": (
        "केवल वही पूंजी दर्ज करें जो आप वास्तव में इस व्यवसाय में लगा सकते हैं।", "ಈ ವ್ಯವಹಾರಕ್ಕೆ ನೀವು ನಿಜವಾಗಿ ತೊಡಗಿಸಬಹುದಾದ ಬಂಡವಾಳವನ್ನು ಮಾತ್ರ ನಮೂದಿಸಿ."),
    "Enter people who can reliably work on the activity when needed.": (
        "जरूरत पड़ने पर गतिविधि पर भरोसे से काम कर सकने वाले लोगों की संख्या दर्ज करें।", "ಅಗತ್ಯವಿದ್ದಾಗ ಚಟುವಟಿಕೆಯಲ್ಲಿ ವಿಶ್ವಾಸದಿಂದ ಕೆಲಸ ಮಾಡಬಲ್ಲ ಜನರ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ."),
    "Enter usable area, not total owned land if part is unavailable.": (
        "उपयोग योग्य क्षेत्र दर्ज करें, कुल स्वामित्व वाली भूमि नहीं यदि उसका कुछ भाग अनुपलब्ध है।", "ಬಳಸಬಹುದಾದ ವಿಸ್ತೀರ್ಣ ನಮೂದಿಸಿ; ಒಂದು ಭಾಗ ಲಭ್ಯವಿಲ್ಲದಿದ್ದರೆ ಒಟ್ಟು ಸ್ವಂತ ಭೂಮಿ ಅಲ್ಲ."),
    "Enter usable pond/culture area in acres.": ("उपयोग योग्य तालाब/संवर्धन क्षेत्र एकड़ में दर्ज करें।", "ಬಳಸಬಹುದಾದ ಕೊಳ/ಸಾಕಣೆ ವಿಸ್ತೀರ್ಣವನ್ನು ಎಕರೆಗಳಲ್ಲಿ ನಮೂದಿಸಿ."),
    "Enter the capital available for the service/business setup.": (
        "सेवा/व्यवसाय स्थापना के लिए उपलब्ध पूंजी दर्ज करें।", "ಸೇವೆ/ವ್ಯವಹಾರ ಸ್ಥಾಪನೆಗೆ ಲಭ್ಯವಿರುವ ಬಂಡವಾಳ ನಮೂದಿಸಿ."),
    "Select access to dependable animal-health support.": (
        "भरोसेमंद पशु-स्वास्थ्य सहायता तक पहुँच चुनें।", "ವಿಶ್ವಾಸಾರ್ಹ ಪ್ರಾಣಿ-ಆರೋಗ್ಯ ಬೆಂಬಲಕ್ಕೆ ನಿಮ್ಮ ಪ್ರವೇಶವನ್ನು ಆರಿಸಿ."),
}

# ------------------------------------------------------------
# PATTERN RULES for generated sentences.  (regex, Hindi, Kannada)
# {0}, {1} = captured groups (translated automatically).
# ------------------------------------------------------------
GS_PATTERNS = [
    (r"^Provide the most realistic current value for (.+)\.$",
     "{0} के लिए सबसे यथार्थवादी वर्तमान मान दर्ज करें।",
     "{0} ಗಾಗಿ ಅತ್ಯಂತ ವಾಸ್ತವಿಕ ಪ್ರಸ್ತುತ ಮೌಲ್ಯವನ್ನು ನೀಡಿ."),
    (r"^View scheme details · (.+)$",
     "योजना विवरण देखें · {0}", "ಯೋಜನೆಯ ವಿವರಗಳನ್ನು ನೋಡಿ · {0}"),
    (r"^(.+): needs attention before starting\.$",
     "{0}: शुरू करने से पहले ध्यान देने की आवश्यकता है।", "{0}: ಪ್ರಾರಂಭಿಸುವ ಮೊದಲು ಗಮನ ಬೇಕು."),
    (r"^Location filter: (.+?)\. (The candidate list.*)$",
     "स्थान फ़िल्टर: {0}। {1}", "ಸ್ಥಳ ಫಿಲ್ಟರ್: {0}. {1}"),
]

# ------------------------------------------------------------
# CURATED TRANSLATIONS — business options, crops, products, scheme names
# ------------------------------------------------------------
_BIZ_PAIRS = {
    "{}–{} days": ("{0}–{1} दिन", "{0}–{1} ದಿನಗಳು"),
    # domains / activities
    "Agri/Food Processing": ("कृषि/खाद्य प्रसंस्करण", "ಕೃಷಿ/ಆಹಾರ ಸಂಸ್ಕರಣೆ"),
    "Agricultural Equipment Repair": ("कृषि उपकरण मरम्मत", "ಕೃಷಿ ಉಪಕರಣ ದುರಸ್ತಿ"),
    "Agricultural Transport": ("कृषि परिवहन", "ಕೃಷಿ ಸಾರಿಗೆ"),
    "Beekeeping": ("मधुमक्खी पालन", "ಜೇನು ಸಾಕಣೆ"),
    "Custom Farm Services": ("किराये की कृषि सेवाएँ", "ಬಾಡಿಗೆ ಕೃಷಿ ಸೇವೆಗಳು"),
    "Farm Equipment Rental": ("कृषि उपकरण किराया", "ಕೃಷಿ ಉಪಕರಣ ಬಾಡಿಗೆ"),
    "Farm Services": ("कृषि सेवाएँ", "ಕೃಷಿ ಸೇವೆಗಳು"),
    "Grain Milling": ("अनाज पिसाई", "ಧಾನ್ಯ ಗಿರಣಿ"),
    "Horticulture & Nursery": ("बागवानी और नर्सरी", "ತೋಟಗಾರಿಕೆ ಮತ್ತು ನರ್ಸರಿ"),
    "Milk Processing": ("दूध प्रसंस्करण", "ಹಾಲು ಸಂಸ್ಕರಣೆ"),
    "Mushroom Cultivation": ("मशरूम की खेती", "ಅಣಬೆ ಕೃಷಿ"),
    "Oil Extraction": ("तेल निष्कर्षण", "ಎಣ್ಣೆ ಹೊರತೆಗೆಯುವಿಕೆ"),
    "Pickle / Jam / Food Processing": ("अचार / जैम / खाद्य प्रसंस्करण", "ಉಪ್ಪಿನಕಾಯಿ / ಜಾಮ್ / ಆಹಾರ ಸಂಸ್ಕರಣೆ"),
    "Plant Nursery": ("पौध नर्सरी", "ಸಸ್ಯ ನರ್ಸರಿ"),
    "Fruit Nursery": ("फल नर्सरी", "ಹಣ್ಣಿನ ನರ್ಸರಿ"),
    "Flower Nursery": ("फूल नर्सरी", "ಹೂವಿನ ನರ್ಸರಿ"),
    "Sericulture": ("रेशम पालन", "ರೇಷ್ಮೆ ಕೃಷಿ"),
    "Spice Processing": ("मसाला प्रसंस्करण", "ಮಸಾಲೆ ಸಂಸ್ಕರಣೆ"),
    # crops & products
    "Areca nut": ("सुपारी", "ಅಡಿಕೆ"), "Black Pepper": ("काली मिर्च", "ಕಾಳುಮೆಣಸು"), "Pepper": ("काली मिर्च", "ಕಾಳುಮೆಣಸು"),
    "Cardamom": ("इलायची", "ಏಲಕ್ಕಿ"), "Cashew": ("काजू", "ಗೇರುಬೀಜ"), "Coffee": ("कॉफ़ी", "ಕಾಫಿ"),
    "Cowpea": ("लोबिया", "ಅಲಸಂದೆ"), "Commercial Maize": ("व्यावसायिक मक्का", "ವಾಣಿಜ್ಯ ಮೆಕ್ಕೆಜೋಳ"),
    "Fenugreek": ("मेथी", "ಮೆಂತ್ಯ"), "Grapes": ("अंगूर", "ದ್ರಾಕ್ಷಿ"), "Orange": ("संतरा", "ಕಿತ್ತಳೆ"),
    "Pomegranate": ("अनार", "ದಾಳಿಂಬೆ"), "Paddy": ("धान", "ಭತ್ತ"), "Rubber": ("रबर", "ರಬ್ಬರ್"),
    "Safflower": ("कुसुम", "ಕುಸುಬೆ"), "Sesame": ("तिल", "ಎಳ್ಳು"), "Tobacco": ("तंबाकू", "ತಂಬಾಕು"),
    "Mulberry": ("शहतूत", "ಹಿಪ್ಪುನೇರಳೆ"), "Vegetables": ("सब्ज़ियाँ", "ತರಕಾರಿಗಳು"), "Flowers": ("फूल", "ಹೂವುಗಳು"),
    "Jasmine": ("चमेली", "ಮಲ್ಲಿಗೆ"), "Marigold": ("गेंदा", "ಚೆಂಡು ಹೂವು"), "Rose": ("गुलाब", "ಗುಲಾಬಿ"),
    "Gerbera": ("जरबेरा", "ಜರ್ಬೆರಾ"), "Chrysanthemum": ("गुलदाउदी", "ಸೇವಂತಿಗೆ"),
    "Jasmine Plants": ("चमेली के पौधे", "ಮಲ್ಲಿಗೆ ಗಿಡಗಳು"), "Marigold Plants": ("गेंदा के पौधे", "ಚೆಂಡು ಹೂವಿನ ಗಿಡಗಳು"),
    "Rose Plants": ("गुलाब के पौधे", "ಗುಲಾಬಿ ಗಿಡಗಳು"), "Gerbera Plants": ("जरबेरा के पौधे", "ಜರ್ಬೆರಾ ಗಿಡಗಳು"),
    "Chrysanthemum Plants": ("गुलदाउदी के पौधे", "ಸೇವಂತಿಗೆ ಗಿಡಗಳು"),
    "Ornamental Plants": ("सजावटी पौधे", "ಅಲಂಕಾರಿಕ ಸಸ್ಯಗಳು"), "Ornamental Nursery": ("सजावटी नर्सरी", "ಅಲಂಕಾರಿಕ ನರ್ಸರಿ"),
    "Medicinal Plants": ("औषधीय पौधे", "ಔಷಧೀಯ ಸಸ್ಯಗಳು"), "Other commercial crop": ("अन्य व्यावसायिक फसल", "ಇತರ ವಾಣಿಜ್ಯ ಬೆಳೆ"),
    "Banana Planting Material": ("केला रोपण सामग्री", "ಬಾಳೆ ನಾಟಿ ಸಾಮಗ್ರಿ"), "Citrus Saplings": ("नींबूवर्गीय पौधे", "ಸಿಟ್ರಸ್ ಸಸಿಗಳು"),
    "Guava Saplings": ("अमरूद के पौधे", "ಸೀಬೆ ಸಸಿಗಳು"), "Mango Saplings": ("आम के पौधे", "ಮಾವಿನ ಸಸಿಗಳು"),
    "Pomegranate Saplings": ("अनार के पौधे", "ದಾಳಿಂಬೆ ಸಸಿಗಳು"), "Fruit Saplings": ("फल के पौधे", "ಹಣ್ಣಿನ ಸಸಿಗಳು"),
    "Fruit Sapling Nursery": ("फल पौध नर्सरी", "ಹಣ್ಣಿನ ಸಸಿ ನರ್ಸರಿ"), "Vegetable Seedlings": ("सब्ज़ी की पौध", "ತರಕಾರಿ ಸಸಿಗಳು"),
    "Vegetable Seedling Nursery": ("सब्ज़ी पौध नर्सरी", "ತರಕಾರಿ ಸಸಿ ನರ್ಸರಿ"),
    "Button Mushroom": ("बटन मशरूम", "ಬಟನ್ ಅಣಬೆ"), "Milky Mushroom": ("मिल्की मशरूम", "ಮಿಲ್ಕಿ ಅಣಬೆ"),
    "Oyster Mushroom": ("ऑयस्टर मशरूम", "ಆಯ್ಸ್ಟರ್ ಅಣಬೆ"), "Other Edible Mushroom": ("अन्य खाद्य मशरूम", "ಇತರ ಖಾದ್ಯ ಅಣಬೆ"),
    "Apis cerana": ("एपिस सेराना", "ಏಪಿಸ್ ಸೆರಾನಾ"), "Apis mellifera": ("एपिस मेलिफेरा", "ಏಪಿಸ್ ಮೆಲ್ಲಿಫೆರಾ"),
    "Honey Bee Apiary": ("मधुमक्खी पालन केंद्र", "ಜೇನು ಸಾಕಣೆ ಕೇಂದ್ರ"), "Migratory Beekeeping": ("प्रवासी मधुमक्खी पालन", "ವಲಸೆ ಜೇನು ಸಾಕಣೆ"),
    "Mulberry Sericulture": ("शहतूत रेशम पालन", "ಹಿಪ್ಪುನೇರಳೆ ರೇಷ್ಮೆ ಕೃಷಿ"), "Silkworm Rearing": ("रेशमकीट पालन", "ರೇಷ್ಮೆ ಹುಳು ಸಾಕಣೆ"),
    "Cocoon Production": ("कोया उत्पादन", "ಗೂಡು ಉತ್ಪಾದನೆ"),
    "Backyard Poultry": ("घरेलू मुर्गी पालन", "ಹಿತ್ತಲಿನ ಕೋಳಿ ಸಾಕಣೆ"), "Rural Poultry": ("ग्रामीण मुर्गी पालन", "ಗ್ರಾಮೀಣ ಕೋಳಿ ಸಾಕಣೆ"),
    "Broiler": ("ब्रॉयलर", "ಬ್ರಾಯ್ಲರ್"), "Layer": ("लेयर (अंडा मुर्गी)", "ಲೇಯರ್ (ಮೊಟ್ಟೆ ಕೋಳಿ)"), "Poultry": ("मुर्गी पालन", "ಕೋಳಿ ಸಾಕಣೆ"),
    "Goat": ("बकरी", "ಮೇಕೆ"), "Sheep": ("भेड़", "ಕುರಿ"), "Piggery": ("सूअर पालन", "ಹಂದಿ ಸಾಕಣೆ"), "Dairy": ("डेयरी", "ಡೈರಿ"),
    "Breeding Goat": ("प्रजनन बकरी", "ತಳಿ ಮೇಕೆ"), "Breeding Goat Unit": ("प्रजनन बकरी इकाई", "ತಳಿ ಮೇಕೆ ಘಟಕ"),
    "Meat Goat": ("मांस बकरी", "ಮಾಂಸದ ಮೇಕೆ"), "Meat Goat Unit": ("मांस बकरी इकाई", "ಮಾಂಸದ ಮೇಕೆ ಘಟಕ"),
    "Dual-purpose Goat": ("दोहरे उद्देश्य की बकरी", "ದ್ವಿ-ಉದ್ದೇಶ ಮೇಕೆ"), "Dual-purpose Sheep": ("दोहरे उद्देश्य की भेड़", "ದ್ವಿ-ಉದ್ದೇಶ ಕುರಿ"),
    "Sheep Breeding": ("भेड़ प्रजनन", "ಕುರಿ ತಳಿ ಅಭಿವೃದ್ಧಿ"), "Sheep Meat": ("भेड़ का मांस", "ಕುರಿ ಮಾಂಸ"),
    "Dairy Buffalo": ("दुधारू भैंस", "ಹೈನು ಎಮ್ಮೆ"), "Dairy Cattle": ("दुधारू गाय", "ಹೈನು ರಾಸು"), "Mixed Dairy Unit": ("मिश्रित डेयरी इकाई", "ಮಿಶ್ರ ಡೈರಿ ಘಟಕ"),
    "Composite Fish Culture": ("मिश्रित मछली पालन", "ಸಮ್ಮಿಶ್ರ ಮೀನು ಸಾಕಣೆ"), "Freshwater Fish Farming": ("मीठे पानी में मछली पालन", "ಸಿಹಿನೀರಿನ ಮೀನು ಸಾಕಣೆ"),
    "Freshwater Prawn": ("मीठे पानी का झींगा", "ಸಿಹಿನೀರಿನ ಸೀಗಡಿ"), "Catla": ("कतला", "ಕಟ್ಲಾ"), "Rohu": ("रोहू", "ರೋಹು"),
    "Mrigal": ("मृगल", "ಮೃಗಾಲ್"), "Tilapia": ("तिलापिया", "ತಿಲಾಪಿಯಾ"), "Fish Processing": ("मछली प्रसंस्करण", "ಮೀನು ಸಂಸ್ಕರಣೆ"),
    "Fish Retail": ("मछली खुदरा", "ಮೀನು ಚಿಲ್ಲರೆ ಮಾರಾಟ"),
    "Chilli Pickle": ("मिर्च का अचार", "ಮೆಣಸಿನಕಾಯಿ ಉಪ್ಪಿನಕಾಯಿ"), "Lemon Pickle": ("नींबू का अचार", "ನಿಂಬೆ ಉಪ್ಪಿನಕಾಯಿ"),
    "Mango Pickle": ("आम का अचार", "ಮಾವಿನ ಉಪ್ಪಿನಕಾಯಿ"), "Mango Jam": ("आम जैम", "ಮಾವಿನ ಜಾಮ್"), "Guava Jam": ("अमरूद जैम", "ಸೀಬೆ ಜಾಮ್"),
    "Tomato-based Product": ("टमाटर आधारित उत्पाद", "ಟೊಮೇಟೊ ಆಧಾರಿತ ಉತ್ಪನ್ನ"), "Spice Blends": ("मसाला मिश्रण", "ಮಸಾಲೆ ಮಿಶ್ರಣಗಳು"),
    "Chilli Powder": ("मिर्च पाउडर", "ಮೆಣಸಿನ ಪುಡಿ"), "Coriander Powder": ("धनिया पाउडर", "ಕೊತ್ತಂಬರಿ ಪುಡಿ"),
    "Turmeric Powder": ("हल्दी पाउडर", "ಅರಿಶಿನ ಪುಡಿ"), "Ginger Powder": ("अदरक पाउडर", "ಶುಂಠಿ ಪುಡಿ"),
    "Coconut Oil": ("नारियल तेल", "ತೆಂಗಿನ ಎಣ್ಣೆ"), "Groundnut Oil": ("मूंगफली तेल", "ಶೇಂಗಾ ಎಣ್ಣೆ"), "Sesame Oil": ("तिल का तेल", "ಎಳ್ಳೆಣ್ಣೆ"),
    "Soybean Oil": ("सोयाबीन तेल", "ಸೋಯಾಬೀನ್ ಎಣ್ಣೆ"), "Sunflower Oil": ("सूरजमुखी तेल", "ಸೂರ್ಯಕಾಂತಿ ಎಣ್ಣೆ"),
    "Rice Milling": ("चावल मिलिंग", "ಅಕ್ಕಿ ಗಿರಣಿ"), "Maize Milling": ("मक्का मिलिंग", "ಮೆಕ್ಕೆಜೋಳ ಗಿರಣಿ"), "Pulse Milling": ("दाल मिलिंग", "ಬೇಳೆ ಗಿರಣಿ"),
    "Ragi Flour": ("रागी आटा", "ರಾಗಿ ಹಿಟ್ಟು"), "Wheat Flour": ("गेहूँ का आटा", "ಗೋಧಿ ಹಿಟ್ಟು"),
    "Curd": ("दही", "ಮೊಸರು"), "Ghee": ("घी", "ತುಪ್ಪ"), "Paneer": ("पनीर", "ಪನೀರ್"), "Flavoured Milk": ("फ्लेवर्ड दूध", "ಸುವಾಸನೆಯುಕ್ತ ಹಾಲು"),
    "Milk-based Sweets": ("दूध आधारित मिठाइयाँ", "ಹಾಲಿನ ಸಿಹಿತಿಂಡಿಗಳು"), "Meat Processing": ("मांस प्रसंस्करण", "ಮಾಂಸ ಸಂಸ್ಕರಣೆ"),
    "Tractor Rental": ("ट्रैक्टर किराया", "ಟ್ರ್ಯಾಕ್ಟರ್ ಬಾಡಿಗೆ"), "Power Tiller Rental": ("पावर टिलर किराया", "ಪವರ್ ಟಿಲ್ಲರ್ ಬಾಡಿಗೆ"),
    "Rotavator Rental": ("रोटावेटर किराया", "ರೋಟವೇಟರ್ ಬಾಡಿಗೆ"), "Sprayer Rental": ("स्प्रेयर किराया", "ಸಿಂಪಡಣೆ ಯಂತ್ರ ಬಾಡಿಗೆ"),
    "Harvester Rental": ("हार्वेस्टर किराया", "ಕೊಯ್ಲು ಯಂತ್ರ ಬಾಡಿಗೆ"), "Tractor Repair": ("ट्रैक्टर मरम्मत", "ಟ್ರ್ಯಾಕ್ಟರ್ ದುರಸ್ತಿ"),
    "Power Tiller Repair": ("पावर टिलर मरम्मत", "ಪವರ್ ಟಿಲ್ಲರ್ ದುರಸ್ತಿ"), "Sprayer Repair": ("स्प्रेयर मरम्मत", "ಸಿಂಪಡಣೆ ಯಂತ್ರ ದುರಸ್ತಿ"),
    "Pump Repair": ("पंप मरम्मत", "ಪಂಪ್ ದುರಸ್ತಿ"), "Farm Implement Repair": ("कृषि औज़ार मरम्मत", "ಕೃಷಿ ಸಲಕರಣೆ ದುರಸ್ತಿ"),
    "Pickup Transport": ("पिकअप परिवहन", "ಪಿಕಪ್ ಸಾರಿಗೆ"), "Three-wheeler Cargo": ("तिपहिया माल वाहन", "ಮೂರು ಚಕ್ರದ ಸರಕು ವಾಹನ"),
    "Tractor Trolley": ("ट्रैक्टर ट्रॉली", "ಟ್ರ್ಯಾಕ್ಟರ್ ಟ್ರಾಲಿ"), "Cold/Protected Transport": ("शीत/संरक्षित परिवहन", "ತಂಪು/ರಕ್ಷಿತ ಸಾರಿಗೆ"),
    "Post-harvest Services": ("कटाई-उपरांत सेवाएँ", "ಕೊಯ್ಲಿನ ನಂತರದ ಸೇವೆಗಳು"), "Land Preparation": ("भूमि तैयारी", "ಭೂಮಿ ಸಿದ್ಧತೆ"),
    "Harvesting": ("कटाई", "ಕೊಯ್ಲು"), "Sowing": ("बुवाई", "ಬಿತ್ತನೆ"), "Spraying": ("छिड़काव", "ಸಿಂಪಡಣೆ"), "Soil Test": ("मिट्टी जाँच", "ಮಣ್ಣು ಪರೀಕ್ಷೆ"),
    "Fertile loam": ("उपजाऊ दोमट", "ಫಲವತ್ತಾದ ಗೋಡು ಮಣ್ಣು"), "Loam": ("दोमट", "ಗೋಡು ಮಣ್ಣು"), "Sandy loam": ("बलुई दोमट", "ಮರಳು ಗೋಡು ಮಣ್ಣು"),
    "Loose sandy loam": ("ढीली बलुई दोमट", "ಸಡಿಲ ಮರಳು ಗೋಡು ಮಣ್ಣು"), "Well-drained loam": ("अच्छी जल-निकासी वाली दोमट", "ಚೆನ್ನಾಗಿ ನೀರು ಬಸಿಯುವ ಗೋಡು ಮಣ್ಣು"),
    "Medium–High": ("मध्यम–उच्च", "ಮಧ್ಯಮ–ಹೆಚ್ಚು"), "Part-time": ("अंशकालिक", "ಅರೆಕಾಲಿಕ"),
    # requirement / risk labels
    "Animal Feed": ("पशु आहार", "ಪ್ರಾಣಿ ಆಹಾರ"), "Feed & Fodder": ("चारा और आहार", "ಮೇವು ಮತ್ತು ಆಹಾರ"),
    "Animal disease": ("पशु रोग", "ಪ್ರಾಣಿ ರೋಗ"), "Animals, Animal Type": ("पशु, पशु प्रकार", "ಪ್ರಾಣಿಗಳು, ಪ್ರಾಣಿ ಪ್ರಕಾರ"),
    "Available operators": ("उपलब्ध ऑपरेटर", "ಲಭ್ಯವಿರುವ ಆಪರೇಟರ್‌ಗಳು"), "Bee boxes planned": ("नियोजित मधुमक्खी बक्से", "ಯೋಜಿತ ಜೇನು ಪೆಟ್ಟಿಗೆಗಳು"),
    "Beekeeping equipment": ("मधुमक्खी पालन उपकरण", "ಜೇನು ಸಾಕಣೆ ಉಪಕರಣ"), "Boxes, Forage": ("बक्से, चारा", "ಪೆಟ್ಟಿಗೆಗಳು, ಮೇವು"),
    "Business/booking access": ("व्यवसाय/बुकिंग पहुँच", "ವ್ಯವಹಾರ/ಬುಕಿಂಗ್ ಪ್ರವೇಶ"),
    "Certified/quality planting material access": ("प्रमाणित/गुणवत्ता रोपण सामग्री तक पहुँच", "ಪ್ರಮಾಣಿತ/ಗುಣಮಟ್ಟದ ನಾಟಿ ಸಾಮಗ್ರಿ ಲಭ್ಯತೆ"),
    "Cold storage/refrigeration": ("शीत भंडारण/रेफ्रिजरेशन", "ಶೀತಲ ಸಂಗ್ರಹ/ರೆಫ್ರಿಜರೇಶನ್"), "Cold Storage": ("शीत भंडारण", "ಶೀತಲ ಸಂಗ್ರಹ"),
    "Colony loss": ("कॉलोनी हानि", "ವಸಾಹತು ನಷ್ಟ"), "Competition": ("प्रतिस्पर्धा", "ಸ್ಪರ್ಧೆ"), "Demand uncertainty": ("मांग की अनिश्चितता", "ಬೇಡಿಕೆಯ ಅನಿಶ್ಚಿತತೆ"),
    "Demand variability": ("मांग में उतार-चढ़ाव", "ಬೇಡಿಕೆಯ ಏರಿಳಿತ"), "Disease": ("रोग", "ರೋಗ"), "Disease/pest pressure": ("रोग/कीट दबाव", "ರೋಗ/ಕೀಟ ಒತ್ತಡ"),
    "Pests/disease": ("कीट/रोग", "ಕೀಟ/ರೋಗ"), "Driver availability": ("चालक की उपलब्धता", "ಚಾಲಕರ ಲಭ್ಯತೆ"),
    "Drying/processing space": ("सुखाने/प्रसंस्करण की जगह", "ಒಣಗಿಸುವ/ಸಂಸ್ಕರಣೆ ಸ್ಥಳ"), "Equipment already available": ("उपकरण पहले से उपलब्ध", "ಉಪಕರಣ ಈಗಾಗಲೇ ಲಭ್ಯ"),
    "Equipment breakdown": ("उपकरण खराबी", "ಉಪಕರಣ ಕೆಟ್ಟುಹೋಗುವುದು"), "Equipment storage": ("उपकरण भंडारण", "ಉಪಕರಣ ಸಂಗ್ರಹ"),
    "Equipment-capacity risk": ("उपकरण-क्षमता जोखिम", "ಉಪಕರಣ-ಸಾಮರ್ಥ್ಯ ಅಪಾಯ"), "Farmer Demand": ("किसान मांग", "ರೈತರ ಬೇಡಿಕೆ"),
    "Feed and growth risk": ("आहार और वृद्धि जोखिम", "ಆಹಾರ ಮತ್ತು ಬೆಳವಣಿಗೆ ಅಪಾಯ"), "Feed costs": ("आहार लागत", "ಆಹಾರ ವೆಚ್ಚ"),
    "Fish species selected": ("चुनी गई मछली प्रजाति", "ಆಯ್ಕೆ ಮಾಡಿದ ಮೀನು ಜಾತಿ"), "Flowering/forage availability": ("फूल/चारे की उपलब्धता", "ಹೂ/ಮೇವಿನ ಲಭ್ಯತೆ"),
    "Food safety requirements": ("खाद्य सुरक्षा आवश्यकताएँ", "ಆಹಾರ ಸುರಕ್ಷತಾ ಅಗತ್ಯಗಳು"), "Food spoilage": ("खाद्य खराबी", "ಆಹಾರ ಹಾಳಾಗುವಿಕೆ"),
    "Food-processing workspace": ("खाद्य प्रसंस्करण कार्यस्थल", "ಆಹಾರ ಸಂಸ್ಕರಣಾ ಕಾರ್ಯಸ್ಥಳ"), "Fuel access": ("ईंधन की उपलब्धता", "ಇಂಧನ ಲಭ್ಯತೆ"),
    "Fuel costs": ("ईंधन लागत", "ಇಂಧನ ವೆಚ್ಚ"), "Fuel prices": ("ईंधन कीमतें", "ಇಂಧನ ಬೆಲೆಗಳು"),
    "Grinding/processing equipment": ("पिसाई/प्रसंस्करण उपकरण", "ಗ್ರೈಂಡಿಂಗ್/ಸಂಸ್ಕರಣಾ ಉಪಕರಣ"), "Growing room area (sq ft)": ("उगाने के कमरे का क्षेत्र (वर्ग फुट)", "ಬೆಳೆಸುವ ಕೋಣೆ ವಿಸ್ತೀರ್ಣ (ಚ. ಅಡಿ)"),
    "Humidity control": ("आर्द्रता नियंत्रण", "ತೇವಾಂಶ ನಿಯಂತ್ರಣ"), "Income Time": ("आय का समय", "ಆದಾಯದ ಸಮಯ"), "Land Acres": ("भूमि (एकड़)", "ಭೂಮಿ (ಎಕರೆ)"),
    "Leaf availability": ("पत्तों की उपलब्धता", "ಎಲೆ ಲಭ್ಯತೆ"), "Load/storage protection": ("भार/भंडारण सुरक्षा", "ಹೊರೆ/ಸಂಗ್ರಹ ರಕ್ಷಣೆ"),
    "Local demand": ("स्थानीय मांग", "ಸ್ಥಳೀಯ ಬೇಡಿಕೆ"), "Local farmer demand": ("स्थानीय किसान मांग", "ಸ್ಥಳೀಯ ರೈತರ ಬೇಡಿಕೆ"),
    "Low seasonal utilisation": ("मौसमी उपयोग कम", "ಕಡಿಮೆ ಋತುಮಾನ ಬಳಕೆ"), "Maintenance costs": ("रखरखाव लागत", "ನಿರ್ವಹಣಾ ವೆಚ್ಚ"),
    "Milk supply availability": ("दूध आपूर्ति की उपलब्धता", "ಹಾಲು ಪೂರೈಕೆ ಲಭ್ಯತೆ"), "Milk-handling risk": ("दूध-हैंडलिंग जोखिम", "ಹಾಲು ನಿರ್ವಹಣಾ ಅಪಾಯ"),
    "Milling machine available": ("मिलिंग मशीन उपलब्ध", "ಗಿರಣಿ ಯಂತ್ರ ಲಭ್ಯ"), "Mulberry Land": ("शहतूत भूमि", "ಹಿಪ್ಪುನೇರಳೆ ಭೂಮಿ"),
    "Mulberry area (acres)": ("शहतूत क्षेत्र (एकड़)", "ಹಿಪ್ಪುನೇರಳೆ ವಿಸ್ತೀರ್ಣ (ಎಕರೆ)"), "Nursery space (sq ft)": ("नर्सरी जगह (वर्ग फुट)", "ನರ್ಸರಿ ಸ್ಥಳ (ಚ. ಅಡಿ)"),
    "Oil extraction machine": ("तेल निष्कर्षण मशीन", "ಎಣ್ಣೆ ತೆಗೆಯುವ ಯಂತ್ರ"), "Oilseed Supply, Machine": ("तिलहन आपूर्ति, मशीन", "ಎಣ್ಣೆಬೀಜ ಪೂರೈಕೆ, ಯಂತ್ರ"),
    "Oilseed availability": ("तिलहन की उपलब्धता", "ಎಣ್ಣೆಬೀಜ ಲಭ್ಯತೆ"), "Oilseed price": ("तिलहन की कीमत", "ಎಣ್ಣೆಬೀಜ ಬೆಲೆ"),
    "Operational downtime risk": ("संचालन बंदी जोखिम", "ಕಾರ್ಯಾಚರಣೆ ಸ್ಥಗಿತ ಅಪಾಯ"), "Operator/technical labour": ("ऑपरेटर/तकनीकी श्रमिक", "ಆಪರೇಟರ್/ತಾಂತ್ರಿಕ ಕಾರ್ಮಿಕರು"),
    "Packaging availability": ("पैकेजिंग की उपलब्धता", "ಪ್ಯಾಕೇಜಿಂಗ್ ಲಭ್ಯತೆ"), "Packaging cost": ("पैकेजिंग लागत", "ಪ್ಯಾಕೇಜಿಂಗ್ ವೆಚ್ಚ"),
    "Plant Material": ("पौध सामग्री", "ಸಸ್ಯ ಸಾಮಗ್ರಿ"), "Plant mortality": ("पौध मृत्यु दर", "ಸಸಿ ಸಾವಿನ ಪ್ರಮಾಣ"), "Planting material source": ("रोपण सामग्री स्रोत", "ನಾಟಿ ಸಾಮಗ್ರಿ ಮೂಲ"),
    "Pond Area, Water Quality, Species": ("तालाब क्षेत्र, जल गुणवत्ता, प्रजाति", "ಕೊಳ ವಿಸ್ತೀರ್ಣ, ನೀರಿನ ಗುಣಮಟ್ಟ, ಜಾತಿ"),
    "Pond area (acres)": ("तालाब क्षेत्र (एकड़)", "ಕೊಳ ವಿಸ್ತೀರ್ಣ (ಎಕರೆ)"), "Pond type": ("तालाब का प्रकार", "ಕೊಳದ ಪ್ರಕಾರ"),
    "Processing equipment": ("प्रसंस्करण उपकरण", "ಸಂಸ್ಕರಣಾ ಉಪಕರಣ"), "Processing workspace": ("प्रसंस्करण कार्यस्थल", "ಸಂಸ್ಕರಣಾ ಕಾರ್ಯಸ್ಥಳ"),
    "Protected cultivation/structure available": ("संरक्षित खेती/संरचना उपलब्ध", "ರಕ್ಷಿತ ಕೃಷಿ/ರಚನೆ ಲಭ್ಯ"), "Quality compliance": ("गुणवत्ता अनुपालन", "ಗುಣಮಟ್ಟ ಅನುಸರಣೆ"),
    "Raw Material": ("कच्चा माल", "ಕಚ್ಚಾ ವಸ್ತು"), "Raw Material, Grinder": ("कच्चा माल, ग्राइंडर", "ಕಚ್ಚಾ ವಸ್ತು, ಗ್ರೈಂಡರ್"), "Raw-material availability": ("कच्चे माल की उपलब्धता", "ಕಚ್ಚಾ ವಸ್ತು ಲಭ್ಯತೆ"),
    "Raw-material quality": ("कच्चे माल की गुणवत्ता", "ಕಚ್ಚಾ ವಸ್ತು ಗುಣಮಟ್ಟ"), "Raw-material seasonality": ("कच्चे माल की मौसमी उपलब्धता", "ಕಚ್ಚಾ ವಸ್ತು ಋತುಮಾನ"),
    "Rearing Space": ("पालन स्थान", "ಸಾಕಣೆ ಸ್ಥಳ"), "Repair tools": ("मरम्मत औज़ार", "ದುರಸ್ತಿ ಉಪಕರಣಗಳು"), "Road/transport delays": ("सड़क/परिवहन में देरी", "ರಸ್ತೆ/ಸಾರಿಗೆ ವಿಳಂಬ"),
    "Seasonal demand": ("मौसमी मांग", "ಋತುಮಾನ ಬೇಡಿಕೆ"), "Seasonality": ("मौसमी प्रभाव", "ಋತುಮಾನ"), "Service area": ("सेवा क्षेत्र", "ಸೇವಾ ಪ್ರದೇಶ"),
    "Shade": ("छाया", "ನೆರಳು"), "Shade/protected area": ("छाया/संरक्षित क्षेत्र", "ನೆರಳು/ರಕ್ಷಿತ ಪ್ರದೇಶ"), "Soil Health": ("मृदा स्वास्थ्य", "ಮಣ್ಣಿನ ಆರೋಗ್ಯ"),
    "Spare-parts access": ("स्पेयर पार्ट्स की उपलब्धता", "ಬಿಡಿಭಾಗಗಳ ಲಭ್ಯತೆ"), "Substrate/raw material availability": ("सब्सट्रेट/कच्चे माल की उपलब्धता", "ಸಬ್‌ಸ್ಟ್ರೇಟ್/ಕಚ್ಚಾ ವಸ್ತು ಲಭ್ಯತೆ"),
    "Suitable vehicle available": ("उपयुक्त वाहन उपलब्ध", "ಸೂಕ್ತ ವಾಹನ ಲಭ್ಯ"), "Technical skill": ("तकनीकी कौशल", "ತಾಂತ್ರಿಕ ಕೌಶಲ"), "Tools, Technical Skill": ("औज़ार, तकनीकी कौशल", "ಉಪಕರಣಗಳು, ತಾಂತ್ರಿಕ ಕೌಶಲ"),
    "Temperature control": ("तापमान नियंत्रण", "ತಾಪಮಾನ ನಿಯಂತ್ರಣ"), "Tools/machinery available": ("औज़ार/मशीनरी उपलब्ध", "ಉಪಕರಣ/ಯಂತ್ರೋಪಕರಣ ಲಭ್ಯ"),
    "Travel/fuel costs": ("यात्रा/ईंधन लागत", "ಪ್ರಯಾಣ/ಇಂಧನ ವೆಚ್ಚ"), "Vehicle Type": ("वाहन प्रकार", "ವಾಹನ ಪ್ರಕಾರ"), "Vehicle maintenance": ("वाहन रखरखाव", "ವಾಹನ ನಿರ್ವಹಣೆ"),
    "Water Management": ("जल प्रबंधन", "ನೀರು ನಿರ್ವಹಣೆ"), "Water quality assessment": ("जल गुणवत्ता आकलन", "ನೀರಿನ ಗುಣಮಟ್ಟ ಮೌಲ್ಯಮಾಪನ"),
    "Water source": ("जल स्रोत", "ನೀರಿನ ಮೂಲ"), "Weather": ("मौसम", "ಹವಾಮಾನ"), "Workshop space": ("वर्कशॉप की जगह", "ಕಾರ್ಯಾಗಾರ ಸ್ಥಳ"),
    "Workspace available": ("कार्यस्थल उपलब्ध", "ಕಾರ್ಯಸ್ಥಳ ಲಭ್ಯ"), "Rearing space": ("पालन स्थान", "ಸಾಕಣೆ ಸ್ಥಳ"),
    "Depends on species and nursery conditions": ("प्रजाति और नर्सरी की स्थितियों पर निर्भर", "ಜಾತಿ ಮತ್ತು ನರ್ಸರಿ ಪರಿಸ್ಥಿತಿಗಳ ಮೇಲೆ ಅವಲಂಬಿತ"),
    "Follows flowering seasons across locations": ("स्थानों के अनुसार फूलने के मौसम का पालन", "ಸ್ಥಳಗಳಿಗನುಗುಣವಾಗಿ ಹೂಬಿಡುವ ಋತುಗಳನ್ನು ಅನುಸರಿಸುತ್ತದೆ"),
    "Multiple seasonal honey flows possible": ("कई मौसमी शहद प्रवाह संभव", "ಹಲವು ಋತುಮಾನದ ಜೇನು ಹರಿವು ಸಾಧ್ಯ"),
    "Needs heat-stress and water management": ("गर्मी-तनाव और जल प्रबंधन आवश्यक", "ಶಾಖ ಒತ್ತಡ ಮತ್ತು ನೀರು ನಿರ್ವಹಣೆ ಅಗತ್ಯ"),
    "Strong attention to heat and water management": ("गर्मी और जल प्रबंधन पर विशेष ध्यान", "ಶಾಖ ಮತ್ತು ನೀರು ನಿರ್ವಹಣೆಗೆ ವಿಶೇಷ ಗಮನ"),
    "Recurring milk production after calving": ("ब्याने के बाद निरंतर दूध उत्पादन", "ಕರು ಹಾಕಿದ ನಂತರ ನಿರಂತರ ಹಾಲು ಉತ್ಪಾದನೆ"),
    "Saleable stage varies by plant species": ("बिक्री योग्य अवस्था पौधे की प्रजाति पर निर्भर", "ಮಾರಾಟಕ್ಕೆ ಸಿದ್ಧ ಹಂತ ಸಸ್ಯ ಜಾತಿಗೆ ಅನುಗುಣವಾಗಿ ಬದಲಾಗುತ್ತದೆ"),
    "Short-cycle seedling production": ("अल्प-चक्र पौध उत्पादन", "ಕಡಿಮೆ ಅವಧಿಯ ಸಸಿ ಉತ್ಪಾದನೆ"),
    "Species and stocking model dependent": ("प्रजाति और स्टॉकिंग मॉडल पर निर्भर", "ಜಾತಿ ಮತ್ತು ಸ್ಟಾಕಿಂಗ್ ಮಾದರಿಯ ಮೇಲೆ ಅವಲಂಬಿತ"),
    "Species and stocking schedule dependent": ("प्रजाति और स्टॉकिंग कार्यक्रम पर निर्भर", "ಜಾತಿ ಮತ್ತು ಸ್ಟಾಕಿಂಗ್ ವೇಳಾಪಟ್ಟಿಯ ಮೇಲೆ ಅವಲಂಬಿತ"),
    "Species-dependent": ("प्रजाति पर निर्भर", "ಜಾತಿಯನ್ನು ಅವಲಂಬಿಸಿದೆ"), "Varies by plant": ("पौधे के अनुसार भिन्न", "ಸಸ್ಯಕ್ಕೆ ಅನುಗುಣವಾಗಿ ಬದಲಾಗುತ್ತದೆ"),
    "Shed plus adequate water/cooling arrangements": ("शेड के साथ पर्याप्त पानी/शीतलन व्यवस्था", "ಶೆಡ್ ಜೊತೆಗೆ ಸಾಕಷ್ಟು ನೀರು/ತಂಪಾಗಿಸುವ ವ್ಯವಸ್ಥೆ"),
    "Shelter plus controlled breeding area": ("आश्रय के साथ नियंत्रित प्रजनन क्षेत्र", "ಆಶ್ರಯ ಜೊತೆಗೆ ನಿಯಂತ್ರಿತ ತಳಿ ಅಭಿವೃದ್ಧಿ ಪ್ರದೇಶ"),
    "Pond with adequate water management": ("पर्याप्त जल प्रबंधन वाला तालाब", "ಸಾಕಷ್ಟು ನೀರು ನಿರ್ವಹಣೆಯ ಕೊಳ"),
    "Nursery space with shade and irrigation": ("छाया और सिंचाई वाली नर्सरी जगह", "ನೆರಳು ಮತ್ತು ನೀರಾವರಿ ಇರುವ ನರ್ಸರಿ ಸ್ಥಳ"),
    "Protected/managed nursery area": ("संरक्षित/प्रबंधित नर्सरी क्षेत्र", "ರಕ್ಷಿತ/ನಿರ್ವಹಿತ ನರ್ಸರಿ ಪ್ರದೇಶ"),
    "Mulberry acreage plus rearing house": ("शहतूत क्षेत्र के साथ पालन गृह", "ಹಿಪ್ಪುನೇರಳೆ ವಿಸ್ತೀರ್ಣ ಜೊತೆಗೆ ಸಾಕಣೆ ಮನೆ"),
    "Breeding-stock buyers and livestock markets": ("प्रजनन पशु खरीदार और पशु बाज़ार", "ತಳಿ ಪ್ರಾಣಿ ಖರೀದಿದಾರರು ಮತ್ತು ಜಾನುವಾರು ಮಾರುಕಟ್ಟೆಗಳು"),
    "Bulk buyers, processors, direct retail": ("थोक खरीदार, प्रोसेसर, सीधी खुदरा बिक्री", "ಸಗಟು ಖರೀದಿದಾರರು, ಸಂಸ್ಕರಣಾಗಾರರು, ನೇರ ಚಿಲ್ಲರೆ ಮಾರಾಟ"),
    "Cocoon markets, reelers, silk value chain": ("कोया बाज़ार, रीलर, रेशम मूल्य श्रृंखला", "ಗೂಡು ಮಾರುಕಟ್ಟೆಗಳು, ರೀಲರ್‌ಗಳು, ರೇಷ್ಮೆ ಮೌಲ್ಯ ಸರಪಳಿ"),
    "Direct consumers, retailers, processors": ("सीधे उपभोक्ता, खुदरा विक्रेता, प्रोसेसर", "ನೇರ ಗ್ರಾಹಕರು, ಚಿಲ್ಲರೆ ವ್ಯಾಪಾರಿಗಳು, ಸಂಸ್ಕರಣಾಗಾರರು"),
    "Households, landscapers, institutions": ("परिवार, लैंडस्केपर, संस्थाएँ", "ಮನೆಗಳು, ಭೂದೃಶ್ಯ ಗುತ್ತಿಗೆದಾರರು, ಸಂಸ್ಥೆಗಳು"),
    "Milk collection, dairies, local consumers": ("दूध संग्रह, डेयरियाँ, स्थानीय उपभोक्ता", "ಹಾಲು ಸಂಗ್ರಹ, ಡೈರಿಗಳು, ಸ್ಥಳೀಯ ಗ್ರಾಹಕರು"),
    "Vegetable farmers, local growers, FPOs": ("सब्ज़ी किसान, स्थानीय उत्पादक, FPO", "ತರಕಾರಿ ರೈತರು, ಸ್ಥಳೀಯ ಬೆಳೆಗಾರರು, FPO ಗಳು"),
    "Multiple villages": ("कई गाँव", "ಹಲವು ಗ್ರಾಮಗಳು"), "Taluk-wide": ("तालुक-व्यापी", "ತಾಲ್ಲೂಕು ಮಟ್ಟದಲ್ಲಿ"), "Village": ("गाँव", "ಗ್ರಾಮ"),
    # scheme filters / categories / beneficiary types
    "Allied Activity": ("संबद्ध गतिविधि", "ಸಂಬಂಧಿತ ಚಟುವಟಿಕೆ"), "Artisan": ("कारीगर", "ಕುಶಲಕರ್ಮಿ"), "Individual Artisan": ("व्यक्तिगत कारीगर", "ವೈಯಕ್ತಿಕ ಕುಶಲಕರ್ಮಿ"),
    "Business Finance": ("व्यवसाय वित्त", "ವ್ಯವಹಾರ ಹಣಕಾಸು"), "Cluster": ("क्लस्टर", "ಕ್ಲಸ್ಟರ್"), "Cooperative": ("सहकारी", "ಸಹಕಾರಿ"),
    "Crop Insurance": ("फसल बीमा", "ಬೆಳೆ ವಿಮೆ"), "Digital Business": ("डिजिटल व्यवसाय", "ಡಿಜಿಟಲ್ ವ್ಯವಹಾರ"), "E-commerce": ("ई-कॉमर्स", "ಇ-ಕಾಮರ್ಸ್"),
    "Entrepreneurship": ("उद्यमिता", "ಉದ್ಯಮಶೀಲತೆ"), "Existing Business": ("मौजूदा व्यवसाय", "ಈಗಿರುವ ವ್ಯವಹಾರ"), "New Business": ("नया व्यवसाय", "ಹೊಸ ವ್ಯವಹಾರ"),
    "Farm Advisory": ("कृषि सलाह", "ಕೃಷಿ ಸಲಹೆ"), "Farmers": ("किसान", "ರೈತರು"), "Fisheries": ("मत्स्य पालन", "ಮೀನುಗಾರಿಕೆ"), "Handicrafts": ("हस्तशिल्प", "ಕರಕುಶಲ ವಸ್ತುಗಳು"),
    "Incubation": ("इन्क्यूबेशन", "ಇನ್ಕ್ಯುಬೇಶನ್"), "Individual Entrepreneur": ("व्यक्तिगत उद्यमी", "ವೈಯಕ್ತಿಕ ಉದ್ಯಮಿ"), "Individual Farmer": ("व्यक्तिगत किसान", "ವೈಯಕ್ತಿಕ ರೈತ"),
    "Infrastructure": ("अवसंरचना", "ಮೂಲಸೌಕರ್ಯ"), "Innovation": ("नवाचार", "ನಾವೀನ್ಯತೆ"), "Institution": ("संस्था", "ಸಂಸ್ಥೆ"), "Manufacturing": ("विनिर्माण", "ತಯಾರಿಕೆ"),
    "Marketing": ("विपणन", "ಮಾರುಕಟ್ಟೆ ಪ್ರಚಾರ"), "Micro-enterprise": ("सूक्ष्म उद्यम", "ಸೂಕ್ಷ್ಮ ಉದ್ಯಮ"), "Rural Industry": ("ग्रामीण उद्योग", "ಗ್ರಾಮೀಣ ಉದ್ಯಮ"),
    "SHG/Group": ("स्वयं सहायता समूह/समूह", "ಸ್ವಸಹಾಯ ಗುಂಪು/ಗುಂಪು"), "Small Enterprise": ("लघु उद्यम", "ಸಣ್ಣ ಉದ್ಯಮ"), "Small/Marginal Farmer": ("लघु/सीमांत किसान", "ಸಣ್ಣ/ಅತಿ ಸಣ್ಣ ರೈತ"),
    "Tenant Farmer": ("बटाईदार किसान", "ಗೇಣಿದಾರ ರೈತ"), "Traditional Industry": ("पारंपरिक उद्योग", "ಸಾಂಪ್ರದಾಯಿಕ ಉದ್ಯಮ"), "Trading": ("व्यापार", "ವ್ಯಾಪಾರ"),
    # scheme names / agencies
    "Agriculture Infrastructure Fund": ("कृषि अवसंरचना कोष", "ಕೃಷಿ ಮೂಲಸೌಕರ್ಯ ನಿಧಿ"),
    "Credit Guarantee Scheme through CGTMSE": ("CGTMSE के माध्यम से ऋण गारंटी योजना", "CGTMSE ಮೂಲಕ ಸಾಲ ಖಾತರಿ ಯೋಜನೆ"),
    "DAY-NRLM – Deendayal Antyodaya Yojana": ("DAY-NRLM – दीनदयाल अंत्योदय योजना", "DAY-NRLM – ದೀನದಯಾಳ್ ಅಂತ್ಯೋದಯ ಯೋಜನೆ"),
    "Government of India": ("भारत सरकार", "ಭಾರತ ಸರ್ಕಾರ"),
    "MSME TEAM Initiative": ("MSME TEAM पहल", "MSME TEAM ಉಪಕ್ರಮ"),
    "Ministry of New and Renewable Energy": ("नवीन और नवीकरणीय ऊर्जा मंत्रालय", "ನವೀನ ಮತ್ತು ನವೀಕರಿಸಬಹುದಾದ ಇಂಧನ ಸಚಿವಾಲಯ"),
    "Ministry of Rural Development": ("ग्रामीण विकास मंत्रालय", "ಗ್ರಾಮೀಣ ಅಭಿವೃದ್ಧಿ ಸಚಿವಾಲಯ"),
    "National Beekeeping and Honey Mission": ("राष्ट्रीय मधुमक्खी पालन और शहद मिशन", "ರಾಷ್ಟ್ರೀಯ ಜೇನು ಸಾಕಣೆ ಮತ್ತು ಜೇನುತುಪ್ಪ ಮಿಷನ್"),
    "National Beekeeping and Honey Mission (NBHM)": ("राष्ट्रीय मधुमक्खी पालन और शहद मिशन (NBHM)", "ರಾಷ್ಟ್ರೀಯ ಜೇನು ಸಾಕಣೆ ಮತ್ತು ಜೇನುತುಪ್ಪ ಮಿಷನ್ (NBHM)"),
    "National Horticulture Board (NHB) Schemes": ("राष्ट्रीय बागवानी बोर्ड (NHB) योजनाएँ", "ರಾಷ್ಟ್ರೀಯ ತೋಟಗಾರಿಕೆ ಮಂಡಳಿ (NHB) ಯೋಜನೆಗಳು"),
    "National Livestock Mission (NLM)": ("राष्ट्रीय पशुधन मिशन (NLM)", "ರಾಷ್ಟ್ರೀಯ ಜಾನುವಾರು ಮಿಷನ್ (NLM)"),
    "PM MUDRA Yojana (PMMY)": ("पीएम मुद्रा योजना (PMMY)", "ಪಿಎಂ ಮುದ್ರಾ ಯೋಜನೆ (PMMY)"),
    "Pradhan Mantri MUDRA Yojana (PMMY)": ("प्रधानमंत्री मुद्रा योजना (PMMY)", "ಪ್ರಧಾನ ಮಂತ್ರಿ ಮುದ್ರಾ ಯೋಜನೆ (PMMY)"),
    "PM SVANidhi": ("पीएम स्वनिधि", "ಪಿಎಂ ಸ್ವನಿಧಿ"), "PM Vishwakarma Scheme": ("पीएम विश्वकर्मा योजना", "ಪಿಎಂ ವಿಶ್ವಕರ್ಮ ಯೋಜನೆ"),
    "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)": ("पीएम-किसान (प्रधानमंत्री किसान सम्मान निधि)", "ಪಿಎಂ-ಕಿಸಾನ್ (ಪ್ರಧಾನ ಮಂತ್ರಿ ಕಿಸಾನ್ ಸಮ್ಮಾನ್ ನಿಧಿ)"),
    "PMKSY – Per Drop More Crop (Micro Irrigation)": ("PMKSY – प्रति बूँद अधिक फसल (सूक्ष्म सिंचाई)", "PMKSY – ಪ್ರತಿ ಹನಿಗೆ ಹೆಚ್ಚು ಬೆಳೆ (ಸೂಕ್ಷ್ಮ ನೀರಾವರಿ)"),
    "Pradhan Mantri Fasal Bima Yojana (PMFBY)": ("प्रधानमंत्री फसल बीमा योजना (PMFBY)", "ಪ್ರಧಾನ ಮಂತ್ರಿ ಫಸಲ್ ಬಿಮಾ ಯೋಜನೆ (PMFBY)"),
    "Pradhan Mantri Matsya Sampada Yojana (PMMSY)": ("प्रधानमंत्री मत्स्य संपदा योजना (PMMSY)", "ಪ್ರಧಾನ ಮಂತ್ರಿ ಮತ್ಸ್ಯ ಸಂಪದ ಯೋಜನೆ (PMMSY)"),
    "Soil Health Card / Soil Health & Fertility": ("मृदा स्वास्थ्य कार्ड / मृदा स्वास्थ्य और उर्वरता", "ಮಣ್ಣು ಆರೋಗ್ಯ ಕಾರ್ಡ್ / ಮಣ್ಣಿನ ಆರೋಗ್ಯ ಮತ್ತು ಫಲವತ್ತತೆ"),
    "e-NAM (National Agriculture Market)": ("e-NAM (राष्ट्रीय कृषि बाज़ार)", "e-NAM (ರಾಷ್ಟ್ರೀಯ ಕೃಷಿ ಮಾರುಕಟ್ಟೆ)"),
    "DPR, Land details, KYC, Bank application.": ("डीपीआर, भूमि विवरण, केवाईसी, बैंक आवेदन।", "DPR, ಭೂಮಿ ವಿವರಗಳು, KYC, ಬ್ಯಾಂಕ್ ಅರ್ಜಿ."),
    "Eligible street vendors.": ("पात्र रेहड़ी-पटरी विक्रेता।", "ಅರ್ಹ ಬೀದಿ ವ್ಯಾಪಾರಿಗಳು."),
}


GS_PAIRS = {}
GS_PAIRS.update(_UI_PAIRS)
try:
    GS_PAIRS.update(_BIZ_PAIRS)
except NameError:
    pass
try:
    GS_PAIRS.update(_SCHEME_PAIRS)
except NameError:
    pass
GS_I18N = {
    "Hindi": {k: v[0] for k, v in GS_PAIRS.items()},
    "Kannada": {k: v[1] for k, v in GS_PAIRS.items()},
}

# ============================================================
# I18N ENGINE  —  one translation layer for the WHOLE app
# ------------------------------------------------------------
# Every piece of text the app shows (markdown / HTML text nodes, widget
# labels, help text, dropdown options, tabs, expanders, metrics, captions,
# alerts, spinners ...) is routed through this layer, so switching the
# language in the top bar changes the site from start to end.
#
# Lookup order for each piece of text
#   1. curated dictionaries (GS_PAIRS below + the older TEXT / UI_WORD_TR /
#      ENV_UI_TR / OUTPUT_TR / DATA_TR tables already in this file)
#   2. templates with numbers / place names   ("{0} units", "Anekal", ...)
#   3. "Label: value" and "A • B • C" composite text
#   4. optional machine translation (cached in memory + on disk)
#   5. the original English text (never breaks the page)
#
# English is passed through untouched (byte-identical to the old output).
# ============================================================
import inspect as _inspect
import re as _re
import os as _os
import json as _json
import time as _time
import html as _html
import threading as _threading
from concurrent.futures import ThreadPoolExecutor as _GSPool

_GS_LANGS = ("English", "Hindi", "Kannada")
_GS_CODE = {"Hindi": "hi", "Kannada": "kn"}
_GS_NATIVE = _re.compile(r"[\u0900-\u097F\u0C80-\u0CFF]")
_GS_ASCII = _re.compile(r"[A-Za-z]")
_GS_LOWER_WORD = _re.compile(r"[a-z]{3,}")
_GS_NUM = _re.compile(r"₹\s?\d[\d,]*(?:\.\d+)?|\d[\d,]*(?:\.\d+)?\s?%|\d[\d,]*(?:\.\d+)?")
_GS_TAGS = _re.compile(r"(<style\b.*?</style>|<script\b.*?</script>|<!--.*?-->|<[^>]+>)", _re.S | _re.I)
_GS_MD_LINE = _re.compile(r"^(\s*(?:#{1,6}\s+|[-*+]\s+|\d+[.)]\s+|>\s+)?)(.*?)(\s*)$", _re.S)
_GS_MD_STRUCT = _re.compile(r"^\s*(?:#{1,6}\s|[-*+]\s|\d+[.)]\s|>\s|\|)", _re.M)
_GS_DECOR_LEAD = _re.compile(r"^((?:ℹ\ufe0f?|[^\w\s(\[{\"'*_#`<>$₹%+\-–—.,:;!?/&|\\=@~^])+\s*)")
_GS_DECOR_TRAIL = _re.compile(r"(\s*[^\w\s)\]}\"'*_#`<>$₹%+\-–—.,:;!?/&|\\=@~^]+)$")
_GS_KEEP_WORDS = {
    "KCC", "AIF", "MIDH", "NHB", "NLM", "FIDF", "PMFME", "MUDRA", "PMEGP", "NPK", "EMI",
    "API", "CAPEX", "B2B", "AI", "UPI", "GST", "FSSAI", "FPO", "SHG", "NABARD", "APMC",
}

# ------------------------------------------------------------
# language + persistent store (shared by all sessions / reruns)
# ------------------------------------------------------------
def _gs_lang():
    """Active UI language. Reads the language widget first so it is correct
    even on the very rerun in which the user changed it."""
    try:
        ss = st.session_state
        v = ss.get("gs_top_language") or ss.get("language") or "English"
    except Exception:
        v = "English"
    return v if v in _GS_LANGS else "English"


def _gs_cache_path():
    try:
        return Path(__file__).resolve().with_name("gs_translation_cache.json")
    except Exception:
        return None


@st.cache_resource(show_spinner=False)
def _gs_store():
    store = {
        "mt": {},                      # "kn\x1fEnglish text" -> translation
        "fail": 0, "off_until": 0.0,   # circuit breaker for the MT service
        "misses": {"Hindi": set(), "Kannada": set()},
        "lock": _threading.Lock(),
        "dirty": False,
    }
    path = _gs_cache_path()
    try:
        if path is not None and path.exists():
            data = _json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                store["mt"].update({k: v for k, v in data.items() if isinstance(v, str)})
    except Exception:
        pass
    return store


def _gs_secret(name, default=""):
    v = _os.environ.get(name)
    if v:
        return v
    try:
        return str(st.secrets.get(name, default))
    except Exception:
        return default


def _gs_mt_enabled():
    return _gs_secret("GS_AUTO_TRANSLATE", "1").strip().lower() not in ("0", "false", "off", "no") \
        and requests is not None


# ------------------------------------------------------------
# dictionaries -> index
# ------------------------------------------------------------
_GS_RUN = {"index": {}, "place_re": None}     # rebuilt on every script run


def _gs_index(lang):
    got = _GS_RUN["index"].get(lang)
    if got is not None:
        return got
    exact, lower = {}, {}

    def add(d):
        if not isinstance(d, dict):
            return
        for k, v in d.items():
            if isinstance(k, str) and isinstance(v, str) and v.strip() and _GS_ASCII.search(k):
                kk = " ".join(k.split())
                exact.setdefault(kk, v)
                lower.setdefault(kk.lower(), v)

    add(GS_I18N.get(lang))               # curated (highest priority)
    add(GS_PLACES.get(lang))             # place names
    for nm in ("TEXT", "UI_WORD_TR", "ENV_UI_TR", "OUTPUT_TR", "DATA_TR",
               "BUSINESS_DISPLAY_TR", "DYNAMIC_TR", "FIELD_UI_TR", "RISK_UI_TR"):
        tbl = globals().get(nm)
        if isinstance(tbl, dict):
            add(tbl.get(lang))
    _GS_RUN["index"][lang] = (exact, lower)
    return exact, lower


def _gs_lookup(norm, lang):
    exact, lower = _gs_index(lang)
    v = exact.get(norm)
    if v is None:
        v = lower.get(norm.lower())
    if v is not None:
        return v
    # trailing punctuation tolerance ("Crop" <-> "Crop:")
    for tail in (":", ".", "…", "!"):
        if norm.endswith(tail) and len(norm) > 1:
            base = norm[:-1].rstrip()
            v = exact.get(base) or lower.get(base.lower())
            if v is not None:
                return v.rstrip(":.…!") + tail
    # markdown emphasis wrapper: **text** / *text* / __text__
    for w in ("**", "__", "*", "_"):
        if len(norm) > 2 * len(w) and norm.startswith(w) and norm.endswith(w):
            inner = norm[len(w):-len(w)]
            v = exact.get(inner) or lower.get(inner.lower())
            if v is not None:
                return w + v + w
    return None


def _gs_place_regex(lang):
    rx = _GS_RUN["place_re"]
    if rx is None:
        names = sorted(GS_PLACES_EN, key=len, reverse=True)
        rx = _re.compile(r"(?<![A-Za-z])(" + "|".join(_re.escape(n) for n in names) + r")(?![A-Za-z])")
        _GS_RUN["place_re"] = rx
    return rx


# ------------------------------------------------------------
# machine translation (optional long-tail fallback)
# ------------------------------------------------------------
_GS_PROTECT = _re.compile(r"`[^`\n]+`|\]\(https?://[^)\s]+\)|https?://[^\s<>\")]+")


def _gs_mt_call(text, code):
    """One HTTP translation call. Returns text or None. Never raises."""
    try:
        key = _gs_secret("GOOGLE_TRANSLATE_API_KEY", "")
        if key:   # official Cloud Translation API (recommended for production)
            r = requests.post(
                "https://translation.googleapis.com/language/translate/v2",
                params={"key": key},
                data={"q": text, "source": "en", "target": code, "format": "text"},
                timeout=8,
            )
            if r.status_code == 200:
                return _html.unescape(r.json()["data"]["translations"][0]["translatedText"])
            return None
        r = requests.get(
            "https://translate.googleapis.com/translate_a/single",
            params={"client": "gtx", "sl": "en", "tl": code, "dt": "t", "q": text},
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=6,
        )
        if r.status_code != 200:
            return None
        data = r.json()
        out = "".join(seg[0] for seg in data[0] if seg and seg[0])
        return out or None
    except Exception:
        return None


def _gs_mt_one(text, lang):
    store = _gs_store()
    if _time.time() < store["off_until"]:
        return None
    code = _GS_CODE.get(lang)
    if not code:
        return None
    saved = []

    def keep(m):
        saved.append(m.group(0))
        return "{%d}" % (len(saved) - 1)

    masked = _GS_PROTECT.sub(keep, text)
    bold = masked.startswith("**") and masked.endswith("**") and len(masked) > 4
    plain = masked.replace("**", "").replace("__", "")
    if bold:
        plain = plain.strip()
    out = None
    for i in range(2):                               # one retry
        out = _gs_mt_call(plain, code)
        if out:
            break
        _time.sleep(0.25)
    with store["lock"]:
        if not out:
            store["fail"] += 1
            if store["fail"] >= 4:                   # service unreachable: pause 2 min
                store["off_until"] = _time.time() + 120
                store["fail"] = 0
            return None
        store["fail"] = 0
    out = _re.sub(r"\{\s*(\d+)\s*\}", lambda m: saved[int(m.group(1))] if int(m.group(1)) < len(saved) else m.group(0), out)
    if bold:
        out = "**" + out.strip() + "**"
    # reject echoes (service returned English unchanged)
    if _GS_LOWER_WORD.search(text) and not _GS_NATIVE.search(out):
        return None
    return out


def _gs_mt_many(pairs):
    """Translate {(lang, text)} in parallel and store results."""
    store = _gs_store()
    todo = [(l, t) for (l, t) in pairs if (_GS_CODE.get(l, "") + "\x1f" + t) not in store["mt"]]
    if not todo:
        return
    with _GSPool(max_workers=min(8, len(todo))) as pool:
        results = list(pool.map(lambda lt: _gs_mt_one(lt[1], lt[0]), todo))
    added = False
    with store["lock"]:
        for (l, t), out in zip(todo, results):
            if out:
                store["mt"][_GS_CODE[l] + "\x1f" + t] = out
                added = True
        if added:
            store["dirty"] = True
    if added:
        _gs_flush_cache()


def _gs_flush_cache():
    store = _gs_store()
    path = _gs_cache_path()
    if path is None or not store.get("dirty"):
        return
    try:
        with store["lock"]:
            tmp = path.with_suffix(".tmp")
            tmp.write_text(_json.dumps(store["mt"], ensure_ascii=False), encoding="utf-8")
            tmp.replace(path)
            store["dirty"] = False
    except Exception:
        pass


def _gs_mt_lookup(text, lang, collect):
    """Cache read. During the collect pass, remember what still needs MT."""
    store = _gs_store()
    v = store["mt"].get(_GS_CODE.get(lang, "") + "\x1f" + text)
    if v is not None:
        return v
    store["misses"].setdefault(lang, set()).add(text)
    _dump = _os.environ.get("GS_DUMP_MISSES")          # developer aid: list untranslated text
    if _dump:
        try:
            with open(_dump, "a", encoding="utf-8") as fh:
                fh.write(_json.dumps({"lang": lang, "text": text}, ensure_ascii=False) + "\n")
        except Exception:
            pass
    if collect is not None and _gs_mt_enabled() and _time.time() >= store["off_until"]:
        collect.add((lang, text))
    return None


# ------------------------------------------------------------
# translate ONE unit of plain text
# ------------------------------------------------------------
def _gs_untranslatable(norm):
    if "://" in norm or norm.startswith("www."):
        return True
    if _re.fullmatch(r"[\w.\-+]+@[\w.\-]+", norm):
        return True
    if _re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)+", norm):        # code identifier
        return True
    if "{" in norm and "}" in norm and _re.search(r"\{[\w.\[\]'\"]*\}", norm):
        return True                                             # unformatted template
    return not _GS_LOWER_WORD.search(norm)                      # acronyms / codes / numbers


def _gs_template(norm, lang):
    """Replace numbers and known place names by {} and look the template up."""
    args = []
    places = GS_PLACES.get(lang, {})

    def rep_place(m):
        args.append(places.get(m.group(1), m.group(1)))
        return "\x00"

    tmp = _gs_place_regex(lang).sub(rep_place, norm)
    # numbers next (positions must follow the order of appearance in the text)
    pieces = _re.split(r"(\x00)", tmp)
    place_iter = iter(args)
    ordered, key_parts = [], []
    for p in pieces:
        if p == "\x00":
            ordered.append(next(place_iter))
            key_parts.append("{}")
        else:
            def rep_num(m):
                ordered.append(m.group(0))
                return "{}"
            key_parts.append(_GS_NUM.sub(rep_num, p))
    key = "".join(key_parts)
    if not ordered or key == "{}":
        return None
    v = _gs_lookup(key, lang)
    if v is None:
        return None
    try:
        return v.format(*ordered)
    except Exception:
        return None


def _gs_patterns(lang):
    got = _GS_RUN.get("pat_" + lang)
    if got is None:
        got = []
        idx = 1 if lang == "Hindi" else 2
        for row in GS_PATTERNS:
            try:
                got.append((_re.compile(row[0], _re.S), row[idx]))
            except Exception:
                pass
        _GS_RUN["pat_" + lang] = got
    return got


def gs_fmt(template, **kw):
    """Translate an English template that has {named} placeholders, then fill it.
    Used for the few sentences that mix dynamic values with HTML fragments."""
    lang = _gs_lang()
    try:
        if lang != "English":
            hit = _gs_lookup(" ".join(template.split()), lang)
            if hit is not None:
                template = hit
        return template.format(**kw)
    except Exception:
        return template.format(**kw) if kw else template


def tr_place(name):
    """Localised name of a district / taluk (falls back to the English name)."""
    return GS_PLACES.get(_gs_lang(), {}).get(str(name), str(name))


def _gs_unit(norm, lang, collect, depth=0):
    """Translate a whitespace-normalised plain-text unit. None = leave as is."""
    if not _GS_ASCII.search(norm):
        return None
    hit = _gs_lookup(norm, lang)
    if hit is not None:
        return hit
    if depth > 3:
        return None

    # leading / trailing decoration (emoji, bullets, arrows ...)
    m1 = _GS_DECOR_LEAD.match(norm)
    lead = m1.group(1) if m1 else ""
    rest = norm[len(lead):]
    m2 = _GS_DECOR_TRAIL.search(rest)
    trail = m2.group(1) if m2 else ""
    if trail:
        rest = rest[: len(rest) - len(trail)]
    if lead or trail:
        if not _GS_ASCII.search(rest):
            return None
        inner = _gs_unit(rest, lang, collect, depth + 1)
        return None if inner is None else lead + inner + trail

    t = _gs_template(norm, lang)
    if t is not None:
        return t

    # pattern rules: generated sentences such as "Provide the most realistic ... for <field>."
    for rx, tpl in _gs_patterns(lang):
        mm = rx.match(norm)
        if mm:
            groups = [(_gs_unit(g, lang, collect, depth + 1) or g) if _GS_ASCII.search(g) else g
                      for g in mm.groups()]
            try:
                return tpl.format(*groups)
            except Exception:
                pass

    # "1. Activity — 20/100"
    mn = _re.match(r"^(\d+)\.\s+(.+)$", norm)
    if mn and depth < 3:
        rest = _gs_unit(mn.group(2), lang, collect, depth + 1)
        if rest is not None:
            return mn.group(1) + ". " + rest

    # composite "A • B • C", "A | B", "A — B"
    for sep in (" • ", " | ", " — "):
        if sep in norm:
            parts = norm.split(sep)
            outs = [_gs_unit(p.strip(), lang, collect, depth + 1) for p in parts]
            if any(o is not None for o in outs):
                return sep.join(o if o is not None else p for o, p in zip(outs, parts))
            return None

    # "**Bold lead** rest of the sentence"
    mb = _re.match(r"^\*\*(.+?)\*\*(\s*)(.+)$", norm)
    if mb and depth < 3 and _GS_ASCII.search(mb.group(3) + mb.group(1)):
        a = _gs_unit(mb.group(1).strip(), lang, collect, depth + 1)
        b = _gs_unit(mb.group(3).strip(), lang, collect, depth + 1)
        if a is not None or b is not None:
            return "**" + (a if a is not None else mb.group(1)) + "** " + (b if b is not None else mb.group(3))

    # "Label: value"  -> translate the label, keep / translate the value
    if ": " in norm and depth < 3:
        label, value = norm.split(": ", 1)
        if label and len(label) <= 70:
            lab = _gs_lookup(label + ":", lang) or _gs_lookup(label, lang)
            if lab is not None:
                lab = lab.rstrip(":：") + ":"
                val = _gs_unit(value, lang, None, depth + 1) if _GS_ASCII.search(value) else None
                return lab + " " + (val if val is not None else value)

    if _GS_NATIVE.search(norm):
        return _gs_mixed(norm, lang, collect)
    if _gs_untranslatable(norm):
        return None
    return _gs_mt_lookup(norm, lang, collect)


_GS_LATIN_RUN = _re.compile(r"[A-Za-z][A-Za-z0-9'’\-–/&,. ]*[A-Za-z0-9]")


def _gs_mixed(norm, lang, collect):
    """Unit that already contains native script plus leftover English words."""
    changed = False

    def rep(m):
        nonlocal changed
        run = m.group(0)
        if not _GS_LOWER_WORD.search(run) or run in _GS_KEEP_WORDS:
            return run
        t = _gs_lookup(run, lang)
        if t is None and len(run.split()) >= 2:
            t = _gs_mt_lookup(run, lang, collect)
        if t is None:
            return run
        changed = True
        return t

    out = _GS_LATIN_RUN.sub(rep, norm)
    return out if changed else None


def _gs_translate_units(units, lang):
    """units: list of raw strings -> list of translated strings (or the original)."""
    def once(collect):
        res = []
        for raw in units:
            norm = _html.unescape(raw) if "&" in raw else raw
            norm = " ".join(norm.split())
            try:
                res.append(_gs_unit(norm, lang, collect))
            except Exception:
                res.append(None)
        return res

    collect = set()
    first = once(collect)
    if collect:
        _gs_mt_many(collect)
        first = once(None)
    return [r if r is not None else u for r, u in zip(first, units)]


# ------------------------------------------------------------
# markup-aware translation (markdown + HTML)
# ------------------------------------------------------------
def _gs_edge(text):
    core = text.strip()
    if not core:
        return [(False, text)]
    i = text.index(core[0])
    return [(False, text[:i]), (True, core), (False, text[i + len(core):])]


def _gs_pieces(body):
    pieces = []
    for i, part in enumerate(_GS_TAGS.split(body)):
        if i % 2 == 1 or not part:
            if part:
                pieces.append((False, part))
            continue
        if _GS_MD_STRUCT.search(part):
            for j, line in enumerate(part.split("\n")):
                if j:
                    pieces.append((False, "\n"))
                if line.strip().startswith("|"):
                    cells = line.split("|")
                    for k, cell in enumerate(cells):
                        if k:
                            pieces.append((False, "|"))
                        pieces.extend(_gs_edge(cell))
                else:
                    m = _GS_MD_LINE.match(line)
                    if m and m.group(2):
                        pieces.append((False, m.group(1)))
                        pieces.append((True, m.group(2)))
                        pieces.append((False, m.group(3)))
                    else:
                        pieces.append((False, line))
        else:
            pieces.extend(_gs_edge(part))
    return pieces


def _gs_markup(body):
    lang = _gs_lang()
    if lang == "English" or not isinstance(body, str) or not _GS_ASCII.search(body):
        return body
    try:
        pieces = _gs_pieces(body)
        idx = [i for i, (u, t) in enumerate(pieces) if u and _GS_ASCII.search(t)]
        if not idx:
            return body
        outs = _gs_translate_units([pieces[i][1] for i in idx], lang)
        for i, o in zip(idx, outs):
            pieces[i] = (False, o)
        return "".join(t for _, t in pieces)
    except Exception:
        return body


def _gs_label(text, lang=None):
    lang = lang or _gs_lang()
    if lang == "English" or not isinstance(text, str) or not _GS_ASCII.search(text):
        return text
    try:
        lead = text[: len(text) - len(text.lstrip())]
        trail = text[len(text.rstrip()):]
        return lead + _gs_translate_units([text.strip()], lang)[0] + trail
    except Exception:
        return text


def tr_text(text):
    """Public helper: translate any plain string for the active language."""
    return _gs_label(text)


# ------------------------------------------------------------
# Streamlit proxy: translate arguments of every display / widget call
# ------------------------------------------------------------
# spec value:  "m" = markup (markdown/HTML)   "l" = label   "L" = list of labels
#              "f" = compose format_func (option labels)
_GS_SPECS = {
    "markdown": {"body": "m", "help": "l"}, "caption": {"body": "m", "help": "l"},
    "info": {"body": "m", "title": "l"}, "warning": {"body": "m", "title": "l"},
    "success": {"body": "m", "title": "l"}, "error": {"body": "m", "title": "l"},
    "title": {"body": "m", "help": "l"}, "header": {"body": "m", "help": "l"},
    "subheader": {"body": "m", "help": "l"}, "toast": {"body": "l"},
    "metric": {"label": "l", "value": "l", "delta": "l", "help": "l"},
    "button": {"label": "l", "help": "l"}, "download_button": {"label": "l", "help": "l"},
    "link_button": {"label": "l", "help": "l"}, "checkbox": {"label": "l", "help": "l"},
    "toggle": {"label": "l", "help": "l"},
    "text_input": {"label": "l", "help": "l", "placeholder": "l"},
    "text_area": {"label": "l", "help": "l", "placeholder": "l"},
    "number_input": {"label": "l", "help": "l", "placeholder": "l"},
    "slider": {"label": "l", "help": "l"}, "date_input": {"label": "l", "help": "l"},
    "file_uploader": {"label": "l", "help": "l"},
    "selectbox": {"label": "l", "help": "l", "placeholder": "l", "format_func": "f"},
    "radio": {"label": "l", "help": "l", "format_func": "f"},
    "multiselect": {"label": "l", "help": "l", "placeholder": "l", "format_func": "f"},
    "select_slider": {"label": "l", "help": "l", "format_func": "f"},
    "pills": {"label": "l", "help": "l", "format_func": "f"},
    "segmented_control": {"label": "l", "help": "l", "format_func": "f"},
    "expander": {"label": "l"}, "popover": {"label": "l", "help": "l"},
    "status": {"label": "l"}, "spinner": {"text": "l"},
    "tabs": {"tabs": "L"},
}
_GS_CONTAINERS = {"columns": "many", "tabs": "many", "container": "one", "expander": "one",
                  "popover": "one", "status": "one", "form": "one", "empty": "one"}
_GS_SIGS = {}


def _gs_rewrite(fn, name, spec, args, kwargs):
    if name == "write":
        return tuple(_gs_markup(a) if isinstance(a, str) else a for a in args), kwargs
    sig = _GS_SIGS.get(name)
    if sig is None:
        sig = _GS_SIGS[name] = _inspect.signature(fn)
    ba = sig.bind_partial(*args, **kwargs)
    for pname, kind in spec.items():
        if pname not in ba.arguments:
            continue
        v = ba.arguments[pname]
        if kind == "m" and isinstance(v, str):
            ba.arguments[pname] = _gs_markup(v)
        elif kind == "l" and isinstance(v, str):
            ba.arguments[pname] = _gs_label(v)
        elif kind == "L" and isinstance(v, (list, tuple)):
            strs = [x for x in v if isinstance(x, str)]
            done = iter(_gs_translate_units(strs, _gs_lang()) if strs else [])
            ba.arguments[pname] = [next(done) if isinstance(x, str) else x for x in v]
    if "format_func" in spec:
        base = ba.arguments.get("format_func") or str
        lang = _gs_lang()                # captured: the formatter must stay consistent with its options
        try:
            opts = list(ba.arguments.get("options") or [])
            raw = [base(o) for o in opts]
            texts = [r for r in raw if isinstance(r, str)]
            done = _gs_translate_units(list(texts), lang) if texts else []
            table = dict(zip(texts, done))
        except Exception:
            table = {}

        def _ff(x, _base=base, _tab=table, _lang=lang):
            r = _base(x)
            if not isinstance(r, str):
                return r
            return _tab[r] if r in _tab else _gs_label(r, _lang)

        ba.arguments["format_func"] = _ff
    return ba.args, ba.kwargs


class _GSProxy:
    """Wraps `streamlit` (and every container it returns) so that all text is
    translated on its way to the screen. Everything else is forwarded as-is."""

    def __init__(self, real):
        object.__setattr__(self, "_gs_real", real)

    def __getattr__(self, name):
        real = object.__getattribute__(self, "_gs_real")
        attr = getattr(real, name)
        if not callable(attr):
            return _GSProxy(attr) if name == "sidebar" else attr
        spec = _GS_SPECS.get(name)
        cont = _GS_CONTAINERS.get(name)
        if spec is None and cont is None and name != "write":
            return attr

        def inner(*args, **kwargs):
            if _gs_lang() != "English" and (spec is not None or name == "write"):
                try:
                    args, kwargs = _gs_rewrite(attr, name, spec or {}, args, kwargs)
                except Exception:
                    pass
            out = attr(*args, **kwargs)
            if cont == "many" and isinstance(out, (list, tuple)):
                return type(out)(_GSProxy(o) for o in out)
            if cont == "one":
                return _GSProxy(out)
            return out

        inner.__name__ = name
        return inner

    def __setattr__(self, name, value):
        setattr(object.__getattribute__(self, "_gs_real"), name, value)

    def __enter__(self):
        return object.__getattribute__(self, "_gs_real").__enter__()

    def __exit__(self, *exc):
        return object.__getattribute__(self, "_gs_real").__exit__(*exc)

    def __getitem__(self, item):
        return object.__getattribute__(self, "_gs_real")[item]

    def __iter__(self):
        return iter(object.__getattribute__(self, "_gs_real"))


# From here on, every st.* call in this file goes through the translation layer.
st = _GSProxy(st)

AGRI_LOCATION_CROPS = {
    "Bagalkot": ["Jowar", "Cotton", "Sugarcane", "Sunflower", "Grapes"],
    "Ballari": ["Paddy", "Cotton", "Sunflower", "Maize", "Jowar"],
    "Belagavi": ["Sugarcane", "Jowar", "Maize", "Tobacco", "Groundnut"],
    "Bengaluru Rural": ["Ragi", "Vegetables", "Mulberry", "Mango"],
    "Bengaluru Urban": ["Vegetables", "Ragi", "Flowers", "Mulberry"],
    "Bidar": ["Tur", "Soybean", "Sugarcane", "Jowar"],
    "Chamarajanagar": ["Ragi", "Turmeric", "Cotton", "Sugarcane", "Maize"],
    "Chikballapur": ["Ragi", "Groundnut", "Grapes", "Mulberry", "Vegetables"],
    "Chikkamagaluru": ["Coffee", "Pepper", "Cardamom", "Areca nut", "Paddy"],
    "Chitradurga": ["Groundnut", "Maize", "Onion", "Cotton", "Jowar"],
    "Dakshina Kannada": ["Areca nut", "Coconut", "Paddy", "Cashew", "Rubber"],
    "Davanagere": ["Maize", "Cotton", "Areca nut", "Paddy", "Groundnut"],
    "Dharwad": ["Cotton", "Jowar", "Groundnut", "Maize", "Wheat"],
    "Gadag": ["Cotton", "Groundnut", "Jowar", "Chilli", "Sunflower"],
    "Hassan": ["Paddy", "Ragi", "Coffee", "Potato", "Areca nut"],
    "Haveri": ["Cotton", "Maize", "Chilli", "Jowar", "Groundnut"],
    "Kalaburagi": ["Tur", "Jowar", "Cotton", "Sunflower", "Bajra"],
    "Kodagu": ["Coffee", "Pepper", "Cardamom", "Paddy", "Orange"],
    "Kolar": ["Ragi", "Tomato", "Mango", "Groundnut", "Grapes"],
    "Koppal": ["Paddy", "Cotton", "Maize", "Sunflower", "Jowar"],
    "Mandya": ["Sugarcane", "Paddy", "Ragi", "Coconut", "Jowar"],
    "Mysuru": ["Paddy", "Sugarcane", "Ragi", "Tobacco", "Cotton"],
    "Raichur": ["Paddy", "Cotton", "Jowar", "Sunflower", "Groundnut"],
    "Ramanagara": ["Ragi", "Mulberry", "Vegetables", "Maize"],
    "Shivamogga": ["Paddy", "Areca nut", "Sugarcane", "Coconut", "Cotton"],
    "Tumakuru": ["Ragi", "Groundnut", "Coconut", "Areca nut", "Maize"],
    "Udupi": ["Paddy", "Areca nut", "Coconut", "Cashew", "Rubber"],
    "Uttara Kannada": ["Paddy", "Areca nut", "Coconut", "Cashew", "Spices"],
    "Vijayapura": ["Grapes", "Sunflower", "Jowar", "Cotton", "Pomegranate"],
    "Vijayanagara": ["Paddy", "Cotton", "Sunflower", "Maize", "Jowar"],
    "Yadgir": ["Tur", "Cotton", "Paddy", "Jowar", "Sunflower"],
    "Jamkhandi": ["Sugarcane", "Jowar", "Cotton", "Grapes"],
    "Badami": ["Jowar", "Cotton", "Sunflower", "Onion"],
    "Hosapete": ["Paddy", "Banana", "Sugarcane", "Cotton"],
    "Sandur": ["Jowar", "Maize", "Groundnut"],
    "Gokak": ["Sugarcane", "Cotton", "Maize"],
    "Chikkodi": ["Sugarcane", "Tobacco", "Maize"],
    "Athani": ["Sugarcane", "Cotton", "Jowar", "Grapes"],
    "Nelamangala": ["Ragi", "Vegetables", "Coconut"],
    "Devanahalli": ["Grapes", "Mango", "Vegetables"],
    "Doddaballapura": ["Mulberry", "Ragi", "Vegetables"],
    "Anekal": ["Vegetables", "Ragi", "Flowers"],
    "Humnabad": ["Tur", "Sugarcane", "Soybean"],
    "Basavakalyan": ["Jowar", "Tur", "Sugarcane"],
    "Kollegal": ["Cotton", "Turmeric", "Ragi"],
    "Gundlupet": ["Cotton", "Sunflower", "Maize"],
    "Chikballapur Town": ["Grapes", "Mulberry", "Ragi"],
    "Sringeri": ["Coffee", "Areca nut", "Pepper"],
    "Mudigere": ["Coffee", "Cardamom", "Pepper"],
    "Kadur": ["Maize", "Areca nut", "Ragi"],
    "Hiriyur": ["Groundnut", "Onion", "Maize"],
    "Challakere": ["Groundnut", "Jowar", "Onion"],
    "Mangaluru": ["Areca nut", "Coconut", "Cashew", "Paddy"],
    "Puttur": ["Areca nut", "Rubber", "Coconut"],
    "Bantwal": ["Areca nut", "Paddy", "Coconut"],
    "Harihar": ["Areca nut", "Maize", "Cotton"],
    "Channagiri": ["Areca nut", "Maize", "Coconut"],
    "Hubballi": ["Cotton", "Jowar", "Maize"],
    "Kalghatgi": ["Cotton", "Groundnut", "Chilli"],
    "Ron": ["Cotton", "Chilli", "Groundnut"],
    "Sakleshpur": ["Coffee", "Areca nut", "Cardamom", "Paddy"],
    "Arsikere": ["Ragi", "Groundnut", "Potato"],
    "Ranebennur": ["Cotton", "Maize", "Chilli"],
    "Shahapur": ["Tur", "Cotton", "Paddy"],
    "Madikeri": ["Coffee", "Pepper", "Cardamom", "Orange"],
    "Virajpet": ["Coffee", "Pepper", "Paddy"],
    "Malur": ["Ragi", "Tomato", "Mango"],
    "Srinivaspur": ["Mango", "Groundnut", "Ragi"],
    "Gangavati": ["Paddy", "Cotton", "Maize"],
    "Kunigal": ["Ragi", "Coconut", "Groundnut"],
    "Pandavapura": ["Sugarcane", "Paddy", "Coconut"],
    "Srirangapatna": ["Sugarcane", "Paddy", "Ragi"],
    "Hunsur": ["Tobacco", "Paddy", "Cotton"],
    "Nanjangud": ["Paddy", "Sugarcane", "Turmeric"],
    "Manvi": ["Paddy", "Cotton", "Jowar"],
    "Sindhanur": ["Paddy", "Cotton", "Sunflower"],
    "Channapatna": ["Ragi", "Mulberry", "Coconut"],
    "Magadi": ["Ragi", "Groundnut", "Mulberry"],
    "Sagara": ["Areca nut", "Paddy", "Coconut"],
    "Bhadravathi": ["Sugarcane", "Paddy", "Areca nut"],
    "Tiptur": ["Coconut", "Areca nut", "Ragi"],
    "Kundapura": ["Paddy", "Areca nut", "Coconut"],
    "Karkala": ["Areca nut", "Paddy", "Coconut"],
    "Sirsi": ["Areca nut", "Spices", "Paddy"],
    "Karwar": ["Coconut", "Cashew", "Paddy"],
    "Sindagi": ["Jowar", "Grapes", "Sunflower"],
    "Indi": ["Sugarcane", "Grapes", "Jowar"],
}


# ------------------------------------------------------------
# FINAL UI TRANSLATIONS FOR THE CONTEXTUAL SELECTION / IMAGE FEATURES
# ------------------------------------------------------------
TEXT.setdefault("Hindi", {}).update({
    "Context-based selection": "स्थान और जलवायु के आधार पर चयन",
    "Best context matches are shown first.": "स्थान और जलवायु के अनुसार सबसे उपयुक्त विकल्प पहले दिखाए गए हैं।",
    "Selected option details": "चयनित विकल्प का विवरण",
    "Context fit": "संदर्भ अनुकूलता",
    "Why this option fits": "यह विकल्प क्यों उपयुक्त है",
    "Climate compatibility": "जलवायु अनुकूलता",
    "Production / service cycle": "उत्पादन / सेवा चक्र",
    "Space / infrastructure": "स्थान / बुनियादी ढाँचा",
    "Water requirement": "पानी की आवश्यकता",
    "Typical market": "सामान्य बाज़ार",
    "Location and climate automatically applied": "स्थान और जलवायु अपने आप लागू किए गए हैं",
    "Automatic location profile": "स्वचालित स्थान प्रोफ़ाइल",
    "Current location": "वर्तमान स्थान",
    "Climate": "जलवायु",
    "Temperature": "तापमान",
    "Rainfall": "वर्षा",
    "Irrigation baseline": "सिंचाई आधार",
    "Soil nutrients": "मिट्टी के पोषक तत्व",
    "No context-matched options are available; showing the configured options.": "संदर्भ से मेल खाने वाले विकल्प उपलब्ध नहीं हैं; निर्धारित विकल्प दिखाए जा रहे हैं।",
    "High potential impact on output, cost, continuity or safety": "उत्पादन, लागत, निरंतरता या सुरक्षा पर उच्च संभावित प्रभाव",
    "Moderate potential impact on output, cost, continuity or marketability": "उत्पादन, लागत, निरंतरता या बाजार-क्षमता पर मध्यम संभावित प्रभाव",
    "Lower potential impact when routine controls are maintained": "नियमित नियंत्रण बनाए रखने पर कम संभावित प्रभाव",
})
TEXT.setdefault("Kannada", {}).update({
    "Context-based selection": "ಸ್ಥಳ ಮತ್ತು ಹವಾಮಾನದ ಆಧಾರದ ಆಯ್ಕೆ",
    "Best context matches are shown first.": "ಸ್ಥಳ ಮತ್ತು ಹವಾಮಾನಕ್ಕೆ ಹೊಂದುವ ಉತ್ತಮ ಆಯ್ಕೆಗಳನ್ನು ಮೊದಲು ತೋರಿಸಲಾಗಿದೆ.",
    "Selected option details": "ಆಯ್ಕೆ ಮಾಡಿದ ಆಯ್ಕೆಯ ವಿವರಗಳು",
    "Context fit": "ಸಂದರ್ಭ ಹೊಂದಾಣಿಕೆ",
    "Why this option fits": "ಈ ಆಯ್ಕೆ ಏಕೆ ಸೂಕ್ತವಾಗಿದೆ",
    "Climate compatibility": "ಹವಾಮಾನ ಹೊಂದಾಣಿಕೆ",
    "Production / service cycle": "ಉತ್ಪಾದನೆ / ಸೇವಾ ಚಕ್ರ",
    "Space / infrastructure": "ಸ್ಥಳ / ಮೂಲಸೌಕರ್ಯ",
    "Water requirement": "ನೀರಿನ ಅವಶ್ಯಕತೆ",
    "Typical market": "ಸಾಮಾನ್ಯ ಮಾರುಕಟ್ಟೆ",
    "Location and climate automatically applied": "ಸ್ಥಳ ಮತ್ತು ಹವಾಮಾನವನ್ನು ಸ್ವಯಂಚಾಲಿತವಾಗಿ ಅನ್ವಯಿಸಲಾಗಿದೆ",
    "Automatic location profile": "ಸ್ವಯಂಚಾಲಿತ ಸ್ಥಳ ಪ್ರೊಫೈಲ್",
    "Current location": "ಪ್ರಸ್ತುತ ಸ್ಥಳ",
    "Climate": "ಹವಾಮಾನ",
    "Temperature": "ತಾಪಮಾನ",
    "Rainfall": "ಮಳೆ",
    "Irrigation baseline": "ನೀರಾವರಿ ಆಧಾರ",
    "Soil nutrients": "ಮಣ್ಣಿನ ಪೋಷಕಾಂಶಗಳು",
    "No context-matched options are available; showing the configured options.": "ಸಂದರ್ಭಕ್ಕೆ ಹೊಂದುವ ಆಯ್ಕೆಗಳು ಲಭ್ಯವಿಲ್ಲ; ನಿಗದಿಪಡಿಸಿದ ಆಯ್ಕೆಗಳನ್ನು ತೋರಿಸಲಾಗುತ್ತಿದೆ.",
    "High potential impact on output, cost, continuity or safety": "ಉತ್ಪಾದನೆ, ವೆಚ್ಚ, ನಿರಂತರತೆ ಅಥವಾ ಸುರಕ್ಷತೆಯ ಮೇಲೆ ಹೆಚ್ಚಿನ ಸಂಭವನೀಯ ಪರಿಣಾಮ",
    "Moderate potential impact on output, cost, continuity or marketability": "ಉತ್ಪಾದನೆ, ವೆಚ್ಚ, ನಿರಂತರತೆ ಅಥವಾ ಮಾರುಕಟ್ಟೆ ಸಾಮರ್ಥ್ಯದ ಮೇಲೆ ಮಧ್ಯಮ ಸಂಭವನೀಯ ಪರಿಣಾಮ",
    "Lower potential impact when routine controls are maintained": "ನಿಯಮಿತ ನಿಯಂತ್ರಣಗಳನ್ನು ಕಾಯ್ದುಕೊಂಡಾಗ ಕಡಿಮೆ ಸಂಭವನೀಯ ಪರಿಣಾಮ",
})

# -----------------------------
# TOP NAVIGATION (SIDEBAR REMOVED)
# -----------------------------
st.markdown("""
<style>
[data-testid="stSidebar"], [data-testid="collapsedControl"] {
    display:none !important;
}
.block-container, [data-testid="stMainBlockContainer"] {
    max-width:1800px !important;
    width:100% !important;
    padding-left:2rem !important;
    padding-right:2rem !important;
}
div[data-testid="stHorizontalBlock"]:has([data-testid="stRadio"]) {
    position:sticky; top:0; z-index:1000;
    display:flex; align-items:center; gap:18px;
    padding:10px 16px; margin:0 0 22px;
    border-radius:18px;
    background:rgba(255,255,255,.94);
    border:1px solid rgba(46,125,50,.14);
    box-shadow:0 8px 28px rgba(27,94,32,.10);
    backdrop-filter:blur(14px);
}
.gs-global-brand {
    font-size:19px; font-weight:900; color:#2E7D32;
    white-space:nowrap; min-width:175px;
}
div[data-testid="stHorizontalBlock"]:has([data-testid="stRadio"]) .stRadio { margin:0 !important; flex:1; }
div[data-testid="stHorizontalBlock"]:has([data-testid="stRadio"]) .stRadio > label { display:none !important; }
div[data-testid="stHorizontalBlock"]:has([data-testid="stRadio"]) div[role="radiogroup"] {
    display:flex; justify-content:center; gap:4px; flex-wrap:wrap;
}
div[data-testid="stHorizontalBlock"]:has([data-testid="stRadio"]) div[role="radiogroup"] label {
    border-radius:999px !important; padding:7px 11px !important;
    transition:all .2s ease;
}
div[data-testid="stHorizontalBlock"]:has([data-testid="stRadio"]) div[role="radiogroup"] label:hover {
    background:#E8F5E9; transform:translateY(-1px);
}
div[data-testid="stHorizontalBlock"]:has([data-testid="stRadio"]) .stSelectbox { margin:0 !important; min-width:118px; }
div[data-testid="stHorizontalBlock"]:has([data-testid="stRadio"]) .stSelectbox > label { display:none !important; }
@media(max-width:1000px){
    div[data-testid="stHorizontalBlock"]:has([data-testid="stRadio"]){flex-wrap:wrap;}
    .gs-global-brand{min-width:auto;}
    div[data-testid="stHorizontalBlock"]:has([data-testid="stRadio"]) .stRadio{width:100%;order:3;}
}
@media(max-width:650px){
    .block-container, [data-testid="stMainBlockContainer"] {
        padding-left:.7rem !important; padding-right:.7rem !important;
    }
    div[data-testid="stHorizontalBlock"]:has([data-testid="stRadio"]){position:relative;padding:12px;margin-bottom:14px;}
    div[data-testid="stHorizontalBlock"]:has([data-testid="stRadio"]) div[role="radiogroup"]{justify-content:flex-start;overflow-x:auto;flex-wrap:nowrap;padding-bottom:3px;}
}
</style>
""", unsafe_allow_html=True)

LANGUAGE_NAMES = {
    "English": {"English": "English", "Hindi": "Hindi", "Kannada": "Kannada"},
    "Hindi": {"English": "अंग्रेज़ी", "Hindi": "हिंदी", "Kannada": "कन्नड़"},
    "Kannada": {"English": "ಇಂಗ್ಲಿಷ್", "Hindi": "ಹಿಂದಿ", "Kannada": "ಕನ್ನಡ"},
}
def _language_display_name(lang_code, ui_lang):
    return LANGUAGE_NAMES.get(ui_lang, LANGUAGE_NAMES["English"]).get(lang_code, lang_code)

# ------------------------------------------------------------
# PAN-INDIA STATE / UNION-TERRITORY LOCATION
# ------------------------------------------------------------
INDIA_STATE_CROPS = {
    "Andhra Pradesh": ["Rice", "Groundnut", "Cotton", "Chilli", "Maize", "Tobacco", "Sugarcane", "Banana"],
    "Arunachal Pradesh": ["Rice", "Maize", "Millet", "Ginger", "Turmeric", "Orange", "Banana"],
    "Assam": ["Rice", "Tea", "Jute", "Mustard", "Sugarcane", "Potato", "Banana", "Pulses"],
    "Bihar": ["Rice", "Wheat", "Maize", "Potato", "Lentil", "Mustard", "Sugarcane", "Banana"],
    "Chhattisgarh": ["Rice", "Maize", "Pulses", "Soybean", "Groundnut", "Sugarcane", "Vegetables"],
    "Goa": ["Rice", "Cashew", "Coconut", "Arecanut", "Mango", "Banana", "Vegetables"],
    "Gujarat": ["Cotton", "Groundnut", "Wheat", "Bajra", "Castor", "Cumin", "Sugarcane", "Banana"],
    "Haryana": ["Wheat", "Rice", "Cotton", "Mustard", "Bajra", "Sugarcane", "Potato", "Vegetables"],
    "Himachal Pradesh": ["Wheat", "Maize", "Barley", "Apple", "Potato", "Tomato", "Pea", "Rice"],
    "Jharkhand": ["Rice", "Maize", "Pulses", "Groundnut", "Mustard", "Potato", "Vegetables", "Lac"],
    "Karnataka": ["Rice", "Ragi", "Maize", "Jowar", "Cotton", "Sugarcane", "Groundnut", "Coffee", "Arecanut", "Grapes"],
    "Kerala": ["Rice", "Coconut", "Rubber", "Pepper", "Cardamom", "Banana", "Cashew", "Arecanut"],
    "Madhya Pradesh": ["Soybean", "Wheat", "Gram", "Maize", "Rice", "Cotton", "Pulses", "Mustard"],
    "Maharashtra": ["Cotton", "Soybean", "Sugarcane", "Jowar", "Pigeon Pea", "Onion", "Grapes", "Groundnut"],
    "Manipur": ["Rice", "Maize", "Pulses", "Mustard", "Ginger", "Turmeric", "Pineapple", "Orange"],
    "Meghalaya": ["Rice", "Maize", "Potato", "Ginger", "Turmeric", "Pineapple", "Orange", "Banana"],
    "Mizoram": ["Rice", "Maize", "Ginger", "Turmeric", "Banana", "Pineapple", "Passion Fruit", "Vegetables"],
    "Nagaland": ["Rice", "Maize", "Millet", "Pulses", "Ginger", "Turmeric", "Pineapple", "Naga Chilli"],
    "Odisha": ["Rice", "Pulses", "Groundnut", "Mustard", "Sugarcane", "Cotton", "Turmeric", "Vegetables"],
    "Punjab": ["Wheat", "Rice", "Maize", "Cotton", "Mustard", "Potato", "Sugarcane", "Vegetables"],
    "Rajasthan": ["Wheat", "Bajra", "Mustard", "Gram", "Cotton", "Groundnut", "Guar", "Cumin"],
    "Sikkim": ["Large Cardamom", "Rice", "Maize", "Ginger", "Turmeric", "Orange", "Buckwheat", "Vegetables"],
    "Tamil Nadu": ["Rice", "Sugarcane", "Groundnut", "Cotton", "Maize", "Banana", "Coconut", "Turmeric"],
    "Telangana": ["Rice", "Cotton", "Maize", "Soybean", "Groundnut", "Turmeric", "Chilli", "Red Gram"],
    "Tripura": ["Rice", "Rubber", "Pineapple", "Tea", "Jute", "Banana", "Ginger", "Turmeric"],
    "Uttar Pradesh": ["Wheat", "Rice", "Sugarcane", "Potato", "Mustard", "Pulses", "Maize", "Mango"],
    "Uttarakhand": ["Rice", "Wheat", "Maize", "Millet", "Potato", "Apple", "Mandarin", "Vegetables"],
    "West Bengal": ["Rice", "Potato", "Jute", "Wheat", "Mustard", "Tea", "Sugarcane", "Vegetables"],
    "Andaman and Nicobar Islands": ["Coconut", "Rice", "Banana", "Arecanut", "Pineapple", "Vegetables"],
    "Chandigarh": ["Wheat", "Rice", "Maize", "Vegetables", "Potato", "Mustard"],
    "Dadra and Nagar Haveli and Daman and Diu": ["Rice", "Pulses", "Groundnut", "Mango", "Banana", "Vegetables"],
    "Delhi": ["Wheat", "Rice", "Mustard", "Vegetables", "Potato", "Tomato"],
    "Jammu and Kashmir": ["Rice", "Wheat", "Maize", "Apple", "Saffron", "Walnut", "Potato", "Vegetables"],
    "Ladakh": ["Barley", "Wheat", "Pea", "Potato", "Apricot", "Vegetables"],
    "Lakshadweep": ["Coconut", "Banana", "Breadfruit", "Vegetables"],
    "Puducherry": ["Rice", "Groundnut", "Sugarcane", "Cotton", "Banana", "Vegetables"],
}
locations = sorted(INDIA_STATE_CROPS.keys())
AGRI_LOCATION_CROPS = INDIA_STATE_CROPS
CROP_LOCATION_SUITABILITY = AGRI_LOCATION_CROPS
LOCATION_DISTRICT = {state: state for state in locations}
DISTRICT_ALIASES = {state: [state] for state in locations}
_STATE_CONTEXT_VALUES = {
    "Andhra Pradesh": (27, 950, "Tropical / semi-arid", "Medium"), "Arunachal Pradesh": (22, 2500, "Mountain / humid", "High"),
    "Assam": (25, 2200, "Humid", "High"), "Bihar": (26, 1100, "Subtropical", "Medium"),
    "Chhattisgarh": (26, 1300, "Tropical", "Medium"), "Goa": (27, 3000, "Humid tropical", "High"),
    "Gujarat": (28, 800, "Semi-arid", "Limited"), "Haryana": (25, 650, "Semi-arid", "Medium"),
    "Himachal Pradesh": (18, 1200, "Mountain", "Medium"), "Jharkhand": (25, 1300, "Subtropical", "Medium"),
    "Karnataka": (25, 900, "Tropical / semi-arid", "Medium"), "Kerala": (27, 2800, "Humid tropical", "High"),
    "Madhya Pradesh": (26, 950, "Subtropical / semi-arid", "Medium"), "Maharashtra": (27, 1000, "Tropical / semi-arid", "Medium"),
    "Manipur": (24, 1900, "Humid subtropical", "High"), "Meghalaya": (21, 2500, "Humid / high rainfall", "High"),
    "Mizoram": (24, 2500, "Humid tropical", "High"), "Nagaland": (23, 1800, "Humid subtropical", "High"),
    "Odisha": (27, 1450, "Tropical humid", "High"), "Punjab": (24, 650, "Semi-arid", "Medium"),
    "Rajasthan": (27, 450, "Arid / semi-arid", "Limited"), "Sikkim": (16, 2500, "Mountain / humid", "High"),
    "Tamil Nadu": (28, 950, "Tropical", "Medium"), "Telangana": (27, 900, "Tropical / semi-arid", "Medium"),
    "Tripura": (26, 2200, "Humid tropical", "High"), "Uttar Pradesh": (26, 850, "Subtropical", "Medium"),
    "Uttarakhand": (19, 1500, "Mountain / subtropical", "Medium"), "West Bengal": (27, 1700, "Humid subtropical", "High"),
    "Andaman and Nicobar Islands": (28, 3000, "Humid tropical", "High"), "Chandigarh": (24, 1100, "Subtropical", "Medium"),
    "Dadra and Nagar Haveli and Daman and Diu": (27, 1800, "Tropical humid", "High"), "Delhi": (26, 700, "Semi-arid subtropical", "Medium"),
    "Jammu and Kashmir": (16, 1000, "Mountain / temperate", "Medium"), "Ladakh": (8, 100, "Cold arid", "Limited"),
    "Lakshadweep": (28, 1600, "Humid tropical", "High"), "Puducherry": (28, 1200, "Tropical", "Medium"),
}
LOCATION_CONTEXT = {state: {"state": state, "district": state, "climate": vals[2], "temperature_c": vals[0], "rainfall_mm": vals[1], "soil": "State-level planning profile; verify with a local soil test", "water": vals[3], "market_access": "Moderate"} for state, vals in _STATE_CONTEXT_VALUES.items()}

# ============================================================
# GLOBAL NAVIGATION / SHARED PAN-INDIA LOCATION
# ============================================================
# This block is intentionally placed before every page branch so the
# selected State/UT, language and page are available everywhere.
PAGE_OPTIONS = [
    "Home",
    "Market Prices",
    "Government Schemes",
    "Financial Assistant",
    "Business Recommendation",
]

# Restore safe defaults on the first run.
if "gs_top_language" not in st.session_state:
    st.session_state["gs_top_language"] = "English"
if st.session_state.get("gs_top_language") not in LANGUAGE_NAMES:
    st.session_state["gs_top_language"] = "English"

if "gs_top_location" not in st.session_state:
    st.session_state["gs_top_location"] = locations[0]
if st.session_state.get("gs_top_location") not in locations:
    st.session_state["gs_top_location"] = locations[0]

if "gs_top_page" not in st.session_state:
    st.session_state["gs_top_page"] = "Home"
if st.session_state.get("gs_top_page") not in PAGE_OPTIONS:
    st.session_state["gs_top_page"] = "Home"

nav1, nav2, nav3 = st.columns([5.8, 1.35, 2.0])
with nav1:
    page = st.radio(
        "Navigate",
        PAGE_OPTIONS,
        index=PAGE_OPTIONS.index(st.session_state["gs_top_page"]),
        horizontal=True,
        key="gs_top_page",
        label_visibility="collapsed",
    )
with nav2:
    language = st.selectbox(
        "Language",
        list(LANGUAGE_NAMES.keys()),
        index=list(LANGUAGE_NAMES.keys()).index(st.session_state["gs_top_language"]),
        key="gs_top_language",
        label_visibility="collapsed",
    )
with nav3:
    location = st.selectbox(
        "State / Union Territory",
        locations,
        index=locations.index(st.session_state["gs_top_location"]),
        key="gs_top_location",
        label_visibility="collapsed",
        help="This single State/UT location is shared across the entire Gram Sahayak website.",
    )

# Keep the legacy session keys synchronized because older page functions
# in this application read these names.
st.session_state["language"] = language
st.session_state["location"] = location

# The rest of the application uses these plain variables.
T = TEXT.get(language, TEXT["English"])
# ============================================================
# MARKET DATA
# ============================================================

# Demo/sample prices used only for demonstration.
CROP_DATA = {
    "Tomato": {"price": 30, "unit": "kg", "trend": "Increasing", "category": "Vegetable"},
    "Onion": {"price": 35, "unit": "kg", "trend": "Stable", "category": "Vegetable"},
    "Potato": {"price": 28, "unit": "kg", "trend": "Stable", "category": "Vegetable"},
    "Carrot": {"price": 40, "unit": "kg", "trend": "Increasing", "category": "Vegetable"},
    "Beans": {"price": 55, "unit": "kg", "trend": "Increasing", "category": "Vegetable"},

    # 30+ additional crops
    "Brinjal": {"price": 32, "unit": "kg", "trend": "Stable", "category": "Vegetable"},
    "Cabbage": {"price": 24, "unit": "kg", "trend": "Stable", "category": "Vegetable"},
    "Cauliflower": {"price": 38, "unit": "kg", "trend": "Increasing", "category": "Vegetable"},
    "Capsicum": {"price": 62, "unit": "kg", "trend": "Increasing", "category": "Vegetable"},
    "Green Chilli": {"price": 58, "unit": "kg", "trend": "Increasing", "category": "Vegetable"},
    "Lady Finger": {"price": 45, "unit": "kg", "trend": "Stable", "category": "Vegetable"},
    "Bottle Gourd": {"price": 30, "unit": "kg", "trend": "Stable", "category": "Vegetable"},
    "Bitter Gourd": {"price": 48, "unit": "kg", "trend": "Increasing", "category": "Vegetable"},
    "Cucumber": {"price": 30, "unit": "kg", "trend": "Stable", "category": "Vegetable"},
    "Pumpkin": {"price": 22, "unit": "kg", "trend": "Stable", "category": "Vegetable"},
    "Drumstick": {"price": 70, "unit": "kg", "trend": "Increasing", "category": "Vegetable"},
    "Peas": {"price": 65, "unit": "kg", "trend": "Increasing", "category": "Vegetable"},
    "Beetroot": {"price": 36, "unit": "kg", "trend": "Stable", "category": "Vegetable"},
    "Radish": {"price": 26, "unit": "kg", "trend": "Stable", "category": "Vegetable"},
    "Spinach": {"price": 25, "unit": "kg", "trend": "Increasing", "category": "Leafy"},
    "Coriander": {"price": 55, "unit": "kg", "trend": "Increasing", "category": "Leafy"},
    "Fenugreek Leaves": {"price": 48, "unit": "kg", "trend": "Stable", "category": "Leafy"},

    "Maize": {"price": 24, "unit": "kg", "trend": "Stable", "category": "Cereal"},
    "Wheat": {"price": 30, "unit": "kg", "trend": "Stable", "category": "Cereal"},
    "Rice": {"price": 42, "unit": "kg", "trend": "Stable", "category": "Cereal"},
    "Ragi": {"price": 38, "unit": "kg", "trend": "Increasing", "category": "Cereal"},
    "Jowar": {"price": 34, "unit": "kg", "trend": "Increasing", "category": "Cereal"},
    "Bajra": {"price": 32, "unit": "kg", "trend": "Stable", "category": "Cereal"},

    "Groundnut": {"price": 75, "unit": "kg", "trend": "Increasing", "category": "Oilseed"},
    "Sunflower": {"price": 58, "unit": "kg", "trend": "Stable", "category": "Oilseed"},
    "Soybean": {"price": 48, "unit": "kg", "trend": "Stable", "category": "Oilseed"},
    "Tur": {"price": 105, "unit": "kg", "trend": "Increasing", "category": "Pulse"},
    "Green Gram": {"price": 92, "unit": "kg", "trend": "Stable", "category": "Pulse"},
    "Black Gram": {"price": 88, "unit": "kg", "trend": "Stable", "category": "Pulse"},
    "Bengal Gram": {"price": 70, "unit": "kg", "trend": "Stable", "category": "Pulse"},

    "Cotton": {"price": 72, "unit": "kg", "trend": "Increasing", "category": "Commercial"},
    "Sugarcane": {"price": 3.6, "unit": "kg", "trend": "Stable", "category": "Commercial"},
    "Turmeric": {"price": 145, "unit": "kg", "trend": "Increasing", "category": "Spice"},
    "Chilli": {"price": 190, "unit": "kg", "trend": "Increasing", "category": "Spice"},
    "Ginger": {"price": 105, "unit": "kg", "trend": "Increasing", "category": "Spice"},
    "Garlic": {"price": 120, "unit": "kg", "trend": "Stable", "category": "Spice"},
    "Coconut": {"price": 38, "unit": "piece", "trend": "Stable", "category": "Horticulture"},
    "Banana": {"price": 42, "unit": "kg", "trend": "Stable", "category": "Fruit"},
    "Mango": {"price": 65, "unit": "kg", "trend": "Increasing", "category": "Fruit"},
    "Papaya": {"price": 38, "unit": "kg", "trend": "Stable", "category": "Fruit"},
    "Guava": {"price": 55, "unit": "kg", "trend": "Increasing", "category": "Fruit"},
    "Grapes": {"price": 70, "unit": "kg", "trend": "Stable", "category": "Fruit"},
    "Pomegranate": {"price": 110, "unit": "kg", "trend": "Stable", "category": "Fruit"},
    "Orange": {"price": 55, "unit": "kg", "trend": "Stable", "category": "Fruit"},
}

# Location multiplier = demonstration of location-sensitive pricing.
LOCATION_FACTOR = {
    "Hubballi": 1.00,
    "Dharwad": 0.98,
    "Belagavi": 1.03,
    "Bengaluru": 1.18,
    "Mysuru": 1.08,
    "Shivamogga": 1.02,
    "Davanagere": 0.97,
    "Gadag": 0.95,
    "Haveri": 0.96,
    "Vijayapura": 0.94,
    "Kalaburagi": 0.96,
    "Raichur": 0.95,
    "Tumakuru": 1.05,
    "Chitradurga": 0.96,
}

# ============================================================
# LOCATION → SUITABLE CROPS
# ============================================================
CROP_LOCATION_SUITABILITY = AGRI_LOCATION_CROPS

LOCATION_CROP_CATEGORY_ALIASES = {
    "Vegetables": {"Vegetable", "Leafy"}, "Fruits": {"Fruit"}, "Fruit": {"Fruit"},
    "Cereals": {"Cereal"}, "Pulses": {"Pulse"}, "Oilseeds": {"Oilseed"},
    "Spices": {"Spice"}, "Commercial": {"Commercial"}, "Horticulture": {"Horticulture"},
}

def suitable_crops_for_location(loc):
    names = CROP_LOCATION_SUITABILITY.get(loc, [])
    if not names:
        return []
    valid = []
    for item in names:
        if item in CROP_DATA:
            valid.append(item)
            continue
        cats = LOCATION_CROP_CATEGORY_ALIASES.get(item, set())
        if cats:
            valid.extend(crop for crop, data in CROP_DATA.items() if data.get("category") in cats)
    return list(dict.fromkeys(valid))

CROP_CATEGORY_FALLBACK = {"Paddy":"Cereal","Vegetables":"Vegetable","Flowers":"Floriculture","Mulberry":"Commercial","Grapes":"Fruit","Mango":"Fruit","Pomegranate":"Fruit","Orange":"Fruit","Coffee":"Commercial","Pepper":"Spice","Cardamom":"Spice","Areca nut":"Horticulture","Coconut":"Horticulture","Cashew":"Horticulture","Rubber":"Commercial","Tobacco":"Commercial","Spices":"Spice","Potato":"Vegetable"}

def crop_category(crop):
    return CROP_DATA.get(crop, {}).get("category", CROP_CATEGORY_FALLBACK.get(crop, "Other"))

# ============================================================
# BUSINESS PROFILES
# ============================================================

BUSINESSES = [
    {
        "name": "Vegetable Cultivation",
        "capital": (25000, 250000),
        "resources": ["Land", "Water", "Agricultural tools"],
        "interests": ["Farming", "Agriculture", "Vegetables"],
        "locations": ["Hubballi", "Dharwad", "Belagavi", "Shivamogga", "Haveri",
                      "Davanagere", "Gadag", "Vijayapura", "Kalaburagi", "Raichur", "Tumakuru"],
        "investment": "₹25,000 – ₹2.5 lakh",
        "model": "Grow vegetables → sell to local markets, retailers, hotels or direct customers.",
        "risk": "Weather, water availability and price fluctuations.",
        "steps": [
            "Select crops based on local demand and water availability.",
            "Estimate seed, labour, irrigation and transport costs.",
            "Plan more than one sales channel instead of depending on a single buyer."
        ],
        "schemes": ["Kisan Credit Card", "PMEGP", "Agriculture Infrastructure Fund"],
        "success_rate": 65,
        "timeline_months": (4, 8),
        "expected_return_pct": (20, 45),
        "is_crop_based": True,
        "risks": [
            {"category": "Climate", "description": "Erratic rainfall, heat stress or unseasonal rain can damage standing crops.",
             "likelihood": "Medium", "impact": "High",
             "mitigation": "Choose crops matched to local rainfall/water access; consider drip irrigation or mulching where feasible."},
            {"category": "Market", "description": "Vegetable prices can swing sharply within a single season due to oversupply.",
             "likelihood": "High", "impact": "Medium",
             "mitigation": "Sell across more than one channel (mandi, retailers, direct) and avoid growing only one crop."},
            {"category": "Financial", "description": "Input costs (seed, fertiliser, labour) can rise before the harvest is sold.",
             "likelihood": "Medium", "impact": "Medium",
             "mitigation": "Keep a simple cost sheet and a small buffer fund before the first harvest."},
        ],
        "scheme_benefits": {
            "Kisan Credit Card": "Gives access to working-capital credit for seed, fertiliser and irrigation costs each season.",
            "PMEGP": "Can support setup costs if this is structured as a new eligible micro-enterprise.",
            "Agriculture Infrastructure Fund": "Can help finance post-harvest storage or grading facilities to reduce distress selling.",
        },
    },
    {
        "name": "Small Food Processing Unit",
        "capital": (75000, 1000000),
        "resources": ["Kitchen/Workspace", "Food processing equipment", "Raw materials"],
        "interests": ["Food", "Cooking", "Processing", "Snacks"],
        "locations": locations,
        "investment": "₹75,000 – ₹10 lakh+",
        "model": "Convert local produce into higher-value products such as flour, snacks, pickles, spice mixes or packaged foods.",
        "risk": "Food safety, packaging, shelf life and market access.",
        "steps": [
            "Choose one product with a clear local customer segment.",
            "Calculate raw material, packaging, labour and selling costs.",
            "Test a small batch before investing in larger equipment."
        ],
        "schemes": ["PMFME", "MUDRA", "PMEGP"],
        "success_rate": 60,
        "timeline_months": (6, 12),
        "expected_return_pct": (18, 40),
        "is_crop_based": False,
        "risks": [
            {"category": "Operational", "description": "Food safety, hygiene and shelf-life issues can spoil batches or cause customer loss.",
             "likelihood": "Medium", "impact": "High",
             "mitigation": "Follow basic FSSAI hygiene practices and test shelf life before scaling production."},
            {"category": "Market", "description": "Building a reliable customer base for a new packaged product takes time.",
             "likelihood": "High", "impact": "Medium",
             "mitigation": "Start with local haats, retailers and word-of-mouth before wider distribution."},
            {"category": "Financial", "description": "Packaging and raw-material costs can erode thin margins if not tracked closely.",
             "likelihood": "Medium", "impact": "Medium",
             "mitigation": "Cost every batch precisely before setting a selling price."},
        ],
        "scheme_benefits": {
            "PMFME": "Directly targeted at micro food-processing units; may offer credit-linked capital subsidy for eligible individual units.",
            "MUDRA": "Collateral-free credit for equipment, raw material and working capital.",
            "PMEGP": "Useful for setting up a new eligible processing unit with structured project finance.",
        },
    },
    {
        "name": "Grocery & Daily-Needs Store",
        "capital": (100000, 700000),
        "resources": ["Shop space", "Working capital", "Supplier network"],
        "interests": ["Retail", "Shopping", "Customer service", "Trading"],
        "locations": locations,
        "investment": "₹1 lakh – ₹7 lakh",
        "model": "Sell essential household products with repeat local demand.",
        "risk": "Competition, inventory management and credit sales.",
        "steps": [
            "Start with fast-moving essentials instead of excessive inventory.",
            "Track daily sales and stock movement.",
            "Add high-demand local products after observing customer behaviour."
        ],
        "schemes": ["MUDRA", "PMEGP"],
        "success_rate": 70,
        "timeline_months": (3, 6),
        "expected_return_pct": (12, 25),
        "is_crop_based": False,
        "risks": [
            {"category": "Market", "description": "Larger stores or online delivery can undercut prices on fast-moving items.",
             "likelihood": "Medium", "impact": "Medium",
             "mitigation": "Compete on convenience, credit for regulars and personal relationships rather than price alone."},
            {"category": "Operational", "description": "Overstocking slow-moving items ties up working capital.",
             "likelihood": "Medium", "impact": "Medium",
             "mitigation": "Track sales weekly and reorder only fast-moving stock."},
            {"category": "Financial", "description": "Informal credit sales to regular customers can strain cash flow.",
             "likelihood": "Medium", "impact": "Medium",
             "mitigation": "Set a clear credit limit per customer and record it consistently."},
        ],
        "scheme_benefits": {
            "MUDRA": "Working-capital loan to stock inventory and manage day-to-day cash flow.",
            "PMEGP": "Can support initial shop setup if structured as a new eligible enterprise.",
        },
    },
    {
        "name": "Street Food / Snack Business",
        "capital": (30000, 300000),
        "resources": ["Kitchen equipment", "Small stall/shop", "Food preparation skills"],
        "interests": ["Food", "Cooking", "Customer service"],
        "locations": locations,
        "investment": "₹30,000 – ₹3 lakh",
        "model": "Sell affordable snacks or meals at a high-footfall local location.",
        "risk": "Location dependency, hygiene and daily demand variation.",
        "steps": [
            "Choose a small menu with good margins.",
            "Test demand at different times of the day.",
            "Maintain hygiene, consistent quality and simple bookkeeping."
        ],
        "schemes": ["PM SVANidhi", "MUDRA", "PMEGP"],
        "success_rate": 62,
        "timeline_months": (2, 5),
        "expected_return_pct": (20, 50),
        "is_crop_based": False,
        "risks": [
            {"category": "Operational", "description": "Location and footfall drive most of the demand; a poor spot can sink an otherwise good menu.",
             "likelihood": "High", "impact": "High",
             "mitigation": "Test 2–3 candidate locations at different times before committing to one."},
            {"category": "Market", "description": "Daily demand can vary a lot with weather, local events and competition.",
             "likelihood": "High", "impact": "Medium",
             "mitigation": "Keep the menu flexible and prepare quantities based on recent daily sales, not guesses."},
            {"category": "Financial", "description": "Perishable ingredients can lead to daily wastage if overordered.",
             "likelihood": "Medium", "impact": "Medium",
             "mitigation": "Buy small quantities frequently rather than bulk, especially when starting out."},
        ],
        "scheme_benefits": {
            "PM SVANidhi": "Designed specifically for street vendors; provides progressive working-capital loan tranches.",
            "MUDRA": "Can fund a cart, cooking equipment or initial stock.",
            "PMEGP": "An option if this is scaled into a larger structured food outlet.",
        },
    },
    {
        "name": "Dairy / Milk-Based Business",
        "capital": (100000, 800000),
        "resources": ["Cattle", "Fodder", "Water", "Shelter"],
        "interests": ["Dairy", "Livestock", "Agriculture"],
        "locations": locations,
        "investment": "₹1 lakh – ₹8 lakh",
        "model": "Milk production with possible value addition such as curd, paneer or ghee.",
        "risk": "Animal health, feed costs and milk-price changes.",
        "steps": [
            "Estimate feed and veterinary costs before buying animals.",
            "Identify a reliable local milk buyer.",
            "Maintain records of milk yield and animal health."
        ],
        "schemes": ["MUDRA", "Kisan Credit Card", "PMEGP"],
        "success_rate": 68,
        "timeline_months": (6, 10),
        "expected_return_pct": (15, 30),
        "is_crop_based": False,
        "risks": [
            {"category": "Climate", "description": "Heat stress and fodder shortage in dry spells can reduce milk yield.",
             "likelihood": "Medium", "impact": "Medium",
             "mitigation": "Plan a fodder reserve or fodder-crop backup before peak summer."},
            {"category": "Operational", "description": "Animal illness can sharply cut yield or require costly treatment.",
             "likelihood": "Medium", "impact": "High",
             "mitigation": "Keep a vaccination schedule and access to a local veterinarian."},
            {"category": "Market", "description": "Milk procurement prices can change with season and buyer negotiation power.",
             "likelihood": "Medium", "impact": "Medium",
             "mitigation": "Explore a cooperative or multiple buyers instead of one, and consider value-added products like curd or ghee."},
        ],
        "scheme_benefits": {
            "MUDRA": "Can finance cattle purchase, shelter or equipment.",
            "Kisan Credit Card": "Working-capital support for fodder and allied dairy costs.",
            "PMEGP": "An option for a larger structured dairy micro-enterprise.",
        },
    },
    {
        "name": "Goat / Sheep Rearing",
        "capital": (60000, 500000),
        "resources": ["Land", "Shelter", "Livestock care"],
        "interests": ["Livestock", "Farming", "Animal husbandry"],
        "locations": locations,
        "investment": "₹60,000 – ₹5 lakh",
        "model": "Rear animals for meat, breeding or local livestock markets.",
        "risk": "Disease, feed costs and market-price fluctuations.",
        "steps": [
            "Start with a manageable herd size.",
            "Plan vaccination and veterinary care.",
            "Build a buyer network before scaling."
        ],
        "schemes": ["MUDRA", "Kisan Credit Card", "PMEGP"],
        "success_rate": 64,
        "timeline_months": (8, 14),
        "expected_return_pct": (20, 40),
        "is_crop_based": False,
        "risks": [
            {"category": "Operational", "description": "Disease can spread quickly through a herd if not monitored.",
             "likelihood": "Medium", "impact": "High",
             "mitigation": "Regular vaccination and isolating new/sick animals before mixing with the herd."},
            {"category": "Climate", "description": "Fodder and water shortage in dry seasons raises feeding costs.",
             "likelihood": "Medium", "impact": "Medium",
             "mitigation": "Plan fodder storage ahead of the dry season."},
            {"category": "Market", "description": "Livestock prices fluctuate with festival demand and local supply.",
             "likelihood": "Medium", "impact": "Medium",
             "mitigation": "Time sales around known demand peaks (festivals) where possible."},
        ],
        "scheme_benefits": {
            "MUDRA": "Can finance purchase of animals and shelter construction.",
            "Kisan Credit Card": "Supports allied agricultural working-capital needs including feed costs.",
            "PMEGP": "An option for a larger structured livestock enterprise.",
        },
    },
    {
        "name": "Poultry Farming",
        "capital": (80000, 600000),
        "resources": ["Shelter", "Water", "Poultry equipment"],
        "interests": ["Poultry", "Livestock", "Farming"],
        "locations": locations,
        "investment": "₹80,000 – ₹6 lakh",
        "model": "Egg or broiler production for nearby markets.",
        "risk": "Feed costs, disease and price volatility.",
        "steps": [
            "Choose egg or meat production based on local demand.",
            "Calculate feed cost per bird.",
            "Maintain biosecurity and veterinary schedules."
        ],
        "schemes": ["MUDRA", "Kisan Credit Card", "PMEGP"],
        "success_rate": 60,
        "timeline_months": (4, 8),
        "expected_return_pct": (15, 35),
        "is_crop_based": False,
        "risks": [
            {"category": "Operational", "description": "Disease outbreaks (e.g. avian illnesses) can wipe out a flock quickly.",
             "likelihood": "Medium", "impact": "High",
             "mitigation": "Follow biosecurity basics: limit outside visitors, disinfect equipment, isolate sick birds fast."},
            {"category": "Financial", "description": "Feed costs are usually the largest ongoing expense and can rise unexpectedly.",
             "likelihood": "High", "impact": "Medium",
             "mitigation": "Track feed-cost-per-bird and consider bulk-buying feed with neighbouring farmers."},
            {"category": "Market", "description": "Egg/broiler prices can be volatile around festivals and oversupply periods.",
             "likelihood": "Medium", "impact": "Medium",
             "mitigation": "Build relationships with more than one buyer to avoid price dependence on one channel."},
        ],
        "scheme_benefits": {
            "MUDRA": "Can finance shelter, equipment and initial birds/feed.",
            "Kisan Credit Card": "Supports allied agricultural working-capital needs.",
            "PMEGP": "An option for a larger structured poultry enterprise.",
        },
    },
    {
        "name": "Local Delivery & Transport Service",
        "capital": (75000, 600000),
        "resources": ["Two-wheeler/vehicle", "Mobile phone", "Driving skills"],
        "interests": ["Transport", "Delivery", "Customer service"],
        "locations": locations,
        "investment": "₹75,000 – ₹6 lakh",
        "model": "Deliver groceries, farm inputs, medicines or local goods within nearby villages/towns.",
        "risk": "Fuel costs, vehicle maintenance and route density.",
        "steps": [
            "Map villages and shops that need regular delivery.",
            "Start with a defined service radius.",
            "Use simple digital records for orders, fuel and collections."
        ],
        "schemes": ["MUDRA", "PMEGP"],
        "success_rate": 66,
        "timeline_months": (2, 4),
        "expected_return_pct": (15, 30),
        "is_crop_based": False,
        "risks": [
            {"category": "Financial", "description": "Fuel price rises directly cut into thin per-delivery margins.",
             "likelihood": "High", "impact": "Medium",
             "mitigation": "Price deliveries to account for fuel, and bundle multiple orders per trip."},
            {"category": "Operational", "description": "Vehicle breakdown halts income until repaired.",
             "likelihood": "Medium", "impact": "Medium",
             "mitigation": "Keep a basic maintenance schedule and a small repair-fund buffer."},
            {"category": "Market", "description": "Low route density in sparsely populated areas can mean too few orders per trip.",
             "likelihood": "Medium", "impact": "Medium",
             "mitigation": "Map demand carefully before committing to a service radius."},
        ],
        "scheme_benefits": {
            "MUDRA": "Can finance a two-wheeler/vehicle or working capital for fuel and upkeep.",
            "PMEGP": "An option if scaled into a larger structured logistics micro-enterprise.",
        },
    },
    {
        "name": "Tailoring & Garment Service",
        "capital": (30000, 250000),
        "resources": ["Sewing machine", "Workspace", "Tailoring skills"],
        "interests": ["Tailoring", "Fashion", "Handicrafts"],
        "locations": locations,
        "investment": "₹30,000 – ₹2.5 lakh",
        "model": "Alterations, stitching, school uniforms, traditional clothing and small-batch garments.",
        "risk": "Competition and seasonal demand.",
        "steps": [
            "Start with alterations and high-demand local garments.",
            "Build repeat customers through reliable delivery.",
            "Add machines only when order volume justifies them."
        ],
        "schemes": ["PM Vishwakarma", "MUDRA", "PMEGP"],
        "success_rate": 72,
        "timeline_months": (3, 6),
        "expected_return_pct": (15, 30),
        "is_crop_based": False,
        "risks": [
            {"category": "Market", "description": "Competition from ready-made garments can reduce demand for custom stitching.",
             "likelihood": "Medium", "impact": "Medium",
             "mitigation": "Focus on alterations, school uniforms and traditional wear where custom work still wins."},
            {"category": "Operational", "description": "Seasonal demand spikes (festivals, school years) can overload capacity.",
             "likelihood": "Medium", "impact": "Low",
             "mitigation": "Take advance bookings and set realistic delivery timelines during peak seasons."},
            {"category": "Financial", "description": "Machine repair or upgrade costs can be an unplanned expense.",
             "likelihood": "Low", "impact": "Medium",
             "mitigation": "Set aside a small maintenance fund from monthly earnings."},
        ],
        "scheme_benefits": {
            "PM Vishwakarma": "Aimed at traditional artisans/craftspeople; may offer toolkit support and skill development.",
            "MUDRA": "Can finance a sewing machine or workspace setup.",
            "PMEGP": "An option for a larger structured tailoring unit.",
        },
    },
    {
        "name": "Handicrafts & Local Products",
        "capital": (25000, 300000),
        "resources": ["Craft skills", "Raw materials", "Workspace"],
        "interests": ["Handicrafts", "Art", "Crafts"],
        "locations": locations,
        "investment": "₹25,000 – ₹3 lakh",
        "model": "Make baskets, decor, traditional products or locally distinctive handmade goods.",
        "risk": "Demand discovery and inconsistent order volume.",
        "steps": [
            "Identify one product with a clear customer segment.",
            "Create a small catalogue and sample products.",
            "Explore local fairs, retailers and digital selling channels."
        ],
        "schemes": ["PM Vishwakarma", "PMEGP", "MUDRA"],
        "success_rate": 55,
        "timeline_months": (6, 12),
        "expected_return_pct": (10, 30),
        "is_crop_based": False,
        "risks": [
            {"category": "Market", "description": "Discovering steady buyers for handmade products can take longer than expected.",
             "likelihood": "High", "impact": "Medium",
             "mitigation": "Test small batches at local fairs and online marketplaces before scaling production."},
            {"category": "Operational", "description": "Order volumes are often inconsistent month to month.",
             "likelihood": "High", "impact": "Medium",
             "mitigation": "Keep costs low and flexible until a repeatable sales channel is found."},
            {"category": "Financial", "description": "Raw material costs can vary, affecting margins on fixed-price products.",
             "likelihood": "Low", "impact": "Low",
             "mitigation": "Review pricing periodically against current material costs."},
        ],
        "scheme_benefits": {
            "PM Vishwakarma": "Directly aimed at traditional artisans; may offer recognition, training and toolkit support.",
            "PMEGP": "Can support setup costs for a new eligible craft micro-enterprise.",
            "MUDRA": "Working-capital credit for raw materials and small-scale production.",
        },
    },
    {
        "name": "Farm Input & Agri Service Centre",
        "capital": (150000, 1000000),
        "resources": ["Shop", "Agriculture knowledge", "Supplier network"],
        "interests": ["Agriculture", "Retail", "Advisory"],
        "locations": locations,
        "investment": "₹1.5 lakh – ₹10 lakh+",
        "model": "Supply seeds, tools, irrigation accessories and farm-related services.",
        "risk": "Inventory, licensing requirements and seasonal demand.",
        "steps": [
            "Identify the crops and farm needs of nearby villages.",
            "Stock fast-moving inputs first.",
            "Follow all applicable licences and quality requirements."
        ],
        "schemes": ["ACABC", "MUDRA", "PMEGP"],
        "success_rate": 63,
        "timeline_months": (6, 12),
        "expected_return_pct": (12, 25),
        "is_crop_based": False,
        "risks": [
            {"category": "Market", "description": "Demand is closely tied to the local farming season and crop choices.",
             "likelihood": "Medium", "impact": "Medium",
             "mitigation": "Stock a mix of inputs matched to what nearby farmers actually grow."},
            {"category": "Financial", "description": "Carrying too much inventory ties up capital in a seasonal business.",
             "likelihood": "Medium", "impact": "Medium",
             "mitigation": "Stock fast-moving inputs first and reorder based on observed demand."},
            {"category": "Operational", "description": "Licensing and quality-compliance requirements can be a barrier to entry.",
             "likelihood": "Low", "impact": "Medium",
             "mitigation": "Confirm all applicable licences before stocking regulated inputs."},
        ],
        "scheme_benefits": {
            "ACABC": "Specifically supports agri-advisory and agri-business centres with training-linked assistance.",
            "MUDRA": "Working-capital credit for stock and shop setup.",
            "PMEGP": "An option for a larger structured agri-service centre.",
        },
    },
    {
        "name": "Small Repair & Service Centre",
        "capital": (40000, 300000),
        "resources": ["Repair tools", "Workspace", "Technical skill"],
        "interests": ["Repair", "Technology", "Machines", "Electronics"],
        "locations": locations,
        "investment": "₹40,000 – ₹3 lakh",
        "model": "Repair phones, appliances, agricultural equipment or other locally needed items.",
        "risk": "Skill dependency and availability of spare parts.",
        "steps": [
            "Choose one repair category based on local demand.",
            "Keep commonly required spare parts.",
            "Build trust through transparent pricing and service records."
        ],
        "schemes": ["MUDRA", "PMEGP"],
        "success_rate": 68,
        "timeline_months": (3, 6),
        "expected_return_pct": (15, 30),
        "is_crop_based": False,
        "risks": [
            {"category": "Operational", "description": "Skill gaps for newer device types can limit the jobs you can take on.",
             "likelihood": "Medium", "impact": "Medium",
             "mitigation": "Start with one repair category you know well and expand skills gradually."},
            {"category": "Financial", "description": "Spare-part availability and cost can delay jobs and squeeze margins.",
             "likelihood": "Medium", "impact": "Medium",
             "mitigation": "Keep commonly needed parts in stock and build a reliable supplier relationship."},
            {"category": "Market", "description": "Trust takes time to build in a new repair business.",
             "likelihood": "Medium", "impact": "Low",
             "mitigation": "Transparent pricing and honest turnaround estimates build repeat customers."},
        ],
        "scheme_benefits": {
            "MUDRA": "Can finance tools, spare parts inventory and workspace setup.",
            "PMEGP": "An option for a larger structured repair/service centre.",
        },
    },
]

# ============================================================
# GOVERNMENT SCHEMES
# ============================================================


# User-provided government scheme dataset. These records are normalized into the
# existing SCHEMES structure below so the current Government Schemes UI can use
# the richer target/benefit/conditions/documents/source/category metadata.
GOVT_SCHEMES_DATA = [
    {
        "name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
        "target": "Small and marginal farmer families possessing cultivable land.",
        "benefit": "Direct income support of ₹6,000 per year in three equal instalments of ₹2,000.",
        "key_conditions": "Subject to exclusion criteria such as high-income status, institutional landholders, and taxpayers.",
        "documents": "Aadhaar, Bank account details, Land record documents.",
        "source_url": "https://pmkisan.gov.in/",
        "categories": ["Agriculture", "Farmers"],
        "beneficiary_types": ["Individual Farmer", "Small/Marginal Farmer"],
        "business_stages": ["Existing Business", "New Business"],
        "funding_min": 0,
        "funding_max": 10000,
        "keywords": ["farmer", "income", "direct benefit", "agriculture", "land"]
    },
    {
        "name": "Kisan Credit Card (KCC)",
        "target": "Farmers, individual/joint borrowers, tenant farmers, SHGs, and JLGs.",
        "benefit": "Concessional short-term crop loans and working capital for agriculture, dairy, and fisheries.",
        "key_conditions": "Interest subvention available for prompt repayment as per RBI/NABARD guidelines.",
        "documents": "Identity proof, Address proof, Land documents, Crop details.",
        "source_url": "https://www.myscheme.gov.in/schemes/kcc",
        "categories": ["Agriculture", "Allied Activity", "Livestock", "Dairy"],
        "beneficiary_types": ["Individual Farmer", "SHG/Group", "Tenant Farmer"],
        "business_stages": ["Existing Business", "New Business"],
        "funding_min": 10000,
        "funding_max": 300000,
        "keywords": ["loan", "credit", "crop loan", "working capital", "dairy", "kcc"]
    },
    {
        "name": "PM MUDRA Yojana (PMMY)",
        "target": "Non-corporate, non-farm small/micro enterprises in retail, manufacturing, services, and allied agriculture.",
        "benefit": "Collateral-free loans up to ₹10 lakh under Shishu, Kishore, and Tarun categories.",
        "key_conditions": "Loans offered by commercial banks, RRBs, MFIs, and NBFCs based on business viability.",
        "documents": "Business plan, ID proof, Address proof, Bank statements, Equipment quotations.",
        "source_url": "https://www.mudra.org.in/",
        "categories": ["Business Activity", "Retail", "Services", "Food Processing", "Allied Activity"],
        "beneficiary_types": ["Individual Entrepreneur", "Micro-enterprise", "SHG/Group"],
        "business_stages": ["New Business", "Existing Business"],
        "funding_min": 10000,
        "funding_max": 1000000,
        "keywords": ["loan", "mudra", "business", "retail", "shop", "micro enterprise", "credit"]
    },
    {
        "name": "PMEGP (Prime Minister's Employment Generation Programme)",
        "target": "Individuals above 18 years, SHGs, Institutions, and Cooperatives establishing new micro-enterprises.",
        "benefit": "Margin money subsidy ranging from 15% to 35% on eligible project costs.",
        "key_conditions": "Applicable for setting up new micro-enterprises only. Beneficiary contribution is required.",
        "documents": "Project report, ID proof, Caste/Category certificate if applicable, Educational qualification certificate.",
        "source_url": "https://www.kviconline.gov.in/pmegpeportal/",
        "categories": ["Business Activity", "Manufacturing", "Services", "Artisan"],
        "beneficiary_types": ["Individual Entrepreneur", "SHG/Group", "Cooperative"],
        "business_stages": ["New Business"],
        "funding_min": 100000,
        "funding_max": 5000000,
        "keywords": ["subsidy", "pmegp", "new unit", "manufacturing", "service", "kvic", "setup"]
    },
    {
        "name": "PMFME (PM Formalisation of Micro Food Processing Enterprises)",
        "target": "Individual micro food processors, FPOs, SHGs, and Producer Cooperatives.",
        "benefit": "Credit-linked capital subsidy at 35% of eligible project cost up to ₹10 lakh per unit.",
        "key_conditions": "Focuses on food processing, ODOP approach, quality standards, and formalisation.",
        "documents": "ID proof, Business registration/license, FSSAI registration or application, Project report.",
        "source_url": "https://pmfme.mofpi.gov.in/",
        "categories": ["Food Processing", "Business Activity", "Agriculture"],
        "beneficiary_types": ["Individual Entrepreneur", "SHG/Group", "FPO", "Cooperative"],
        "business_stages": ["Existing Business", "New Business"],
        "funding_min": 50000,
        "funding_max": 1000000,
        "keywords": ["food processing", "odop", "pickle", "flour", "snack", "subsidy", "fssai"]
    },
    {
        "name": "PM Vishwakarma Scheme",
        "target": "Artisans and craftspeople working with hands and tools in traditional trades.",
        "benefit": "Skill training, toolkit incentive up to ₹15,000, and collateral-free loan support.",
        "key_conditions": "Applicant must be engaged in an eligible traditional craft trade.",
        "documents": "Aadhaar, Mobile number, Bank details, Ration card / Skill certificate.",
        "source_url": "https://pmvishwakarma.gov.in/",
        "categories": ["Artisan", "Handicrafts", "Services"],
        "beneficiary_types": ["Individual Artisan", "Individual Entrepreneur"],
        "business_stages": ["Existing Business", "New Business"],
        "funding_min": 15000,
        "funding_max": 300000,
        "keywords": ["artisan", "handicraft", "craft", "tailor", "carpenter", "blacksmith", "tools"]
    },
    {
        "name": "Agriculture Infrastructure Fund (AIF)",
        "target": "FPOs, Agriculture Entrepreneurs, Cooperatives, PACS and eligible infrastructure projects.",
        "benefit": "Interest subvention and credit guarantee support for eligible agricultural infrastructure projects.",
        "key_conditions": "For creation of post-harvest management infrastructure and community farming assets.",
        "documents": "DPR, Land details, KYC, Bank application.",
        "source_url": "https://agriinfra.dac.gov.in/",
        "categories": ["Agriculture", "Allied Activity", "Infrastructure"],
        "beneficiary_types": ["FPO", "SHG/Group", "Individual Entrepreneur", "Cooperative"],
        "business_stages": ["New Business", "Existing Business"],
        "funding_min": 200000,
        "funding_max": 20000000,
        "keywords": ["warehouse", "storage", "cold storage", "infrastructure", "fpo", "aif", "agri"]
    }
]


# Additional related government programmes / portals verified against official Government
# sources. These use the same schema so they automatically appear in the filters/table.
GOVT_SCHEMES_DATA.extend([
    {
        "name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
        "target": "Farmers seeking crop insurance coverage for notified crops and areas.",
        "benefit": "Crop insurance protection against specified crop losses under the notified scheme terms.",
        "key_conditions": "Coverage, crops, areas, premium and claim conditions depend on the applicable season and state notification.",
        "documents": "Aadhaar/ID, bank details, land or cultivation details, crop details and applicable insurance documents.",
        "source_url": "https://pmfby.gov.in/",
        "categories": ["Agriculture", "Crop Insurance", "Farmers"],
        "beneficiary_types": ["Individual Farmer", "Small/Marginal Farmer", "Tenant Farmer"],
        "business_stages": ["Existing Business", "New Business"],
        "funding_min": 0,
        "funding_max": 1000000,
        "keywords": ["crop insurance", "insurance", "pmfby", "crop loss", "farmer"]
    },
    {
        "name": "PMKSY – Per Drop More Crop (Micro Irrigation)",
        "target": "Farmers and eligible agricultural beneficiaries adopting micro-irrigation such as drip and sprinkler systems.",
        "benefit": "Supports adoption of micro-irrigation to improve water-use efficiency and crop productivity, subject to applicable assistance rules.",
        "key_conditions": "Assistance and implementation are subject to applicable state/district plans, guidelines and beneficiary conditions.",
        "documents": "Identity proof, land/cultivation details, bank details and documents required by the implementing authority.",
        "source_url": "https://pmksy.gov.in/",
        "categories": ["Agriculture", "Irrigation", "Water Management"],
        "beneficiary_types": ["Individual Farmer", "Small/Marginal Farmer", "FPO", "Cooperative"],
        "business_stages": ["Existing Business", "New Business"],
        "funding_min": 10000,
        "funding_max": 1000000,
        "keywords": ["drip", "sprinkler", "irrigation", "water", "micro irrigation", "pmksy"]
    },
    {
        "name": "Soil Health Card / Soil Health & Fertility",
        "target": "Farmers who need soil nutrient assessment and fertilizer/soil-amendment recommendations.",
        "benefit": "Provides soil nutrient status and recommendations for appropriate fertilizer and soil amendments.",
        "key_conditions": "Implementation is through government/state agriculture systems and soil testing facilities.",
        "documents": "Farm/plot details, location, crop information and sample-related details as required by the soil testing system.",
        "source_url": "https://soilhealth.dac.gov.in/",
        "categories": ["Agriculture", "Soil Health", "Farm Advisory"],
        "beneficiary_types": ["Individual Farmer", "Small/Marginal Farmer", "FPO", "Cooperative"],
        "business_stages": ["Existing Business", "New Business"],
        "funding_min": 0,
        "funding_max": 100000,
        "keywords": ["soil", "soil health", "soil test", "fertilizer", "nutrients", "ph", "npk"]
    },
    {
        "name": "e-NAM (National Agriculture Market)",
        "target": "Farmers, traders, FPOs and other eligible participants using integrated agricultural markets.",
        "benefit": "Electronic trading platform connecting APMC markets and supporting transparent price discovery and online agricultural trade.",
        "key_conditions": "Registration, market participation and trading are subject to applicable e-NAM/APMC and state requirements.",
        "documents": "Registration and market-specific documents as required by the relevant e-NAM/APMC process.",
        "source_url": "https://enam.gov.in/",
        "categories": ["Agriculture", "Market Access", "Trading", "FPO"],
        "beneficiary_types": ["Individual Farmer", "FPO", "Individual Entrepreneur", "Cooperative"],
        "business_stages": ["Existing Business", "New Business"],
        "funding_min": 0,
        "funding_max": 0,
        "keywords": ["enam", "e-nam", "mandi", "market", "trading", "price discovery", "fpo"]
    },
])


GOVT_SCHEMES_DATA.extend([
    {
        "name": "National Livestock Mission (NLM)",
        "target": "Eligible entrepreneurs, farmers, FPOs, SHGs and other eligible entities in poultry, sheep, goat, piggery, and feed/fodder activities.",
        "benefit": "Supports entrepreneurship and breed-development activities in rural poultry, sheep, goat and piggery, along with feed and fodder activities, subject to applicable guidelines.",
        "key_conditions": "Activity, beneficiary type, project structure and assistance are governed by the current NLM guidelines and implementing process.",
        "documents": "Identity/KYC documents, land or project details, bank details, project proposal/DPR and other documents required by the implementing authority.",
        "source_url": "https://dahd.gov.in/schemes/programmes/national_livestock_mission",
        "categories": ["Poultry", "Livestock", "Goat", "Sheep", "Piggery", "Feed & Fodder"],
        "beneficiary_types": ["Individual Farmer", "Individual Entrepreneur", "FPO", "SHG/Group"],
        "business_stages": ["New Business", "Existing Business"],
        "funding_min": 50000,
        "funding_max": 10000000,
        "keywords": ["poultry", "chicken", "goat", "sheep", "pig", "piggery", "livestock", "fodder", "feed", "nlm"]
    },
    {
        "name": "Animal Husbandry Infrastructure Development Fund (AHIDF)",
        "target": "Eligible entrepreneurs, MSMEs, FPOs, private companies, Section 8 companies and dairy cooperatives working on animal-husbandry infrastructure.",
        "benefit": "Supports eligible investments in dairy/meat processing, animal feed, breed improvement, veterinary facilities and animal-waste-to-wealth infrastructure under applicable guidelines.",
        "key_conditions": "Eligibility, project categories, financing and current availability must be verified against the latest AHIDF guidelines and implementing authority.",
        "documents": "DPR/project proposal, KYC, business/entity documents, land/project details, bank documents and other lender/department requirements.",
        "source_url": "https://www.dahd.gov.in/schemes/programmes/ahidf",
        "categories": ["Dairy", "Livestock", "Poultry", "Meat Processing", "Animal Feed", "Infrastructure"],
        "beneficiary_types": ["Individual Entrepreneur", "Micro-enterprise", "FPO", "Cooperative"],
        "business_stages": ["New Business", "Existing Business"],
        "funding_min": 500000,
        "funding_max": 100000000,
        "keywords": ["ahidf", "dairy processing", "milk", "meat processing", "animal feed", "poultry feed", "veterinary", "waste to wealth"]
    },
    {
        "name": "Credit Guarantee Scheme through CGTMSE", 
        "target": "Eligible micro and small enterprises seeking institutional credit where credit guarantee support is applicable.",
        "benefit": "Credit guarantee support to eligible lending institutions for qualifying MSE credit facilities, helping improve access to institutional finance.",
        "key_conditions": "Guarantee coverage, eligible borrower, lender, credit facility and applicable limits depend on the current CGTMSE scheme and lender process.",
        "documents": "Udyam/business documents, KYC, project/business details, financial information and documents required by the lending institution.",
        "source_url": "https://www.cgtmse.in/",
        "categories": ["MSME", "Business Finance", "Manufacturing", "Services", "Retail"],
        "beneficiary_types": ["Individual Entrepreneur", "Micro-enterprise", "Small Enterprise"],
        "business_stages": ["New Business", "Existing Business"],
        "funding_min": 0,
        "funding_max": 0,
        "keywords": ["cgtmse", "credit guarantee", "collateral", "loan", "msme", "micro enterprise", "small enterprise"]
    },
    {
        "name": "SFURTI – Scheme of Fund for Regeneration of Traditional Industries",
        "target": "Traditional artisans, rural industries, clusters and implementing agencies working with traditional industry activities.",
        "benefit": "Cluster-based support for regeneration, competitiveness, common facilities, skills, design, technology and market support for traditional industries.",
        "key_conditions": "Typically implemented through approved cluster/project structures rather than as a simple individual cash benefit; current portal and guidelines apply.",
        "documents": "Cluster/project proposal, artisan/enterprise details, implementing-agency documents and documents required under current SFURTI guidelines.",
        "source_url": "https://sfurti.msme.gov.in/",
        "categories": ["Artisan", "Handicrafts", "Rural Industry", "Traditional Industry", "Cluster"],
        "beneficiary_types": ["Individual Artisan", "SHG/Group", "Cooperative", "Cluster"],
        "business_stages": ["New Business", "Existing Business"],
        "funding_min": 0,
        "funding_max": 50000000,
        "keywords": ["sfurti", "artisan", "handicraft", "khadi", "traditional industry", "cluster", "rural industry"]
    },
    {
        "name": "ASPIRE – Innovation, Rural Industry & Entrepreneurship",
        "target": "Eligible institutions and entrepreneurship/incubation initiatives supporting rural innovation and enterprise development.",
        "benefit": "Supports rural entrepreneurship, incubation and innovation ecosystems intended to create employment and enterprise opportunities.",
        "key_conditions": "Support is generally routed through eligible institutions/incubation mechanisms; current programme guidelines determine eligibility.",
        "documents": "Institution/project proposal, registration documents, project plan and documents required by the implementing agency.",
        "source_url": "https://dashboard.msme.gov.in/aspire.aspx",
        "categories": ["Rural Industry", "Entrepreneurship", "Innovation", "Incubation"],
        "beneficiary_types": ["Individual Entrepreneur", "Institution", "SHG/Group", "Cooperative"],
        "business_stages": ["New Business", "Existing Business"],
        "funding_min": 0,
        "funding_max": 0,
        "keywords": ["aspire", "rural industry", "innovation", "incubation", "entrepreneurship", "msme"]
    },
    {
        "name": "MSME TEAM Initiative",
        "target": "Micro and small enterprises seeking digital market access, visibility, e-commerce and marketing support.",
        "benefit": "Supports MSME market access through digital enablement, visibility, training and related market-linkage activities under the RAMP programme.",
        "key_conditions": "Eligibility and available support depend on current TEAM programme guidelines and participating ecosystem partners.",
        "documents": "Udyam/business details, KYC and digital/business information required by the programme or participating platform.",
        "source_url": "https://ramp.msme.gov.in/ramp/",
        "categories": ["MSME", "Digital Business", "Market Access", "E-commerce", "Marketing"],
        "beneficiary_types": ["Individual Entrepreneur", "Micro-enterprise", "Small Enterprise"],
        "business_stages": ["New Business", "Existing Business"],
        "funding_min": 0,
        "funding_max": 1000000,
        "keywords": ["team", "msme team", "digital marketing", "ecommerce", "market access", "online sales", "marketing"]
    },
    {
        "name": "Pradhan Mantri Matsya Sampada Yojana (PMMSY)",
        "target": "Fish farmers, fishers, aquaculture entrepreneurs and eligible fisheries-sector beneficiaries and groups.",
        "benefit": "Supports fisheries production, aquaculture, post-harvest infrastructure, value chains, technology and eligible fisheries activities under the scheme components.",
        "key_conditions": "Eligible activities, assistance pattern and beneficiary contribution depend on the applicable PMMSY component and state/implementing guidelines.",
        "documents": "KYC, fisheries/aquaculture activity details, land/water/project documents, bank details and component-specific documents.",
        "source_url": "https://pmmsy.dof.gov.in/",
        "categories": ["Fisheries", "Aquaculture", "Fish Processing", "Cold Storage", "Fish Retail"],
        "beneficiary_types": ["Individual Entrepreneur", "Individual Farmer", "FPO", "SHG/Group", "Cooperative"],
        "business_stages": ["New Business", "Existing Business"],
        "funding_min": 0,
        "funding_max": 0,
        "keywords": ["pmmsy", "fish", "fisheries", "aquaculture", "biofloc", "hatchery", "fish processing", "cold storage"]
    },
])

BASE_SCHEMES = [
    {
        "name": "PMEGP – Prime Minister's Employment Generation Programme",
        "best_for": "New micro-enterprises in manufacturing and eligible service/non-farm activities.",
        "description": "A credit-linked government programme that supports new micro-enterprises through bank finance and margin-money subsidy. It is designed to create self-employment and employment opportunities, especially for rural and aspiring entrepreneurs.",
        "key": "For new enterprises; applicant generally must be 18+. Project and eligibility conditions apply.",
        "why": "Useful when the entrepreneur is starting a new eligible micro-enterprise and needs structured project finance.",
        "source": "KVIC / Ministry of MSME"
    },
    {
        "name": "Pradhan Mantri MUDRA Yojana (PMMY)",
        "best_for": "Small businesses needing working capital or business expansion finance.",
        "description": "Provides collateral-free institutional credit for eligible micro enterprises in manufacturing, trading, services and allied agricultural activities.",
        "key": "Shishu up to ₹50,000; Kishor above ₹50,000 to ₹5 lakh; Tarun above ₹5 lakh to ₹10 lakh; Tarun Plus above ₹10 lakh to ₹20 lakh for eligible repeat borrowers.",
        "why": "Useful for shops, services, food businesses, livestock-related activities and other eligible micro businesses.",
        "source": "Department of Financial Services, Ministry of Finance"
    },
    {
        "name": "PM SVANidhi",
        "best_for": "Eligible street vendors.",
        "description": "A micro-credit and support programme for street vendors. The restructured scheme includes progressive working-capital loans, digital adoption incentives and broader livelihood support.",
        "key": "Loan tranches can go up to ₹15,000, ₹25,000 and ₹50,000, subject to scheme conditions. Lending period has been extended to March 31, 2030.",
        "why": "Especially relevant for small street food, vending and mobile retail businesses.",
        "source": "Ministry of Housing & Urban Affairs / Government of India"
    },
    {
        "name": "PMFME – Pradhan Mantri Formalisation of Micro Food Processing Enterprises",
        "best_for": "Micro food-processing businesses and eligible SHGs/FPOs/cooperatives.",
        "description": "Supports formalisation, upgrading and capacity building for micro food-processing enterprises. Eligible individual units can receive credit-linked capital subsidy subject to scheme conditions.",
        "key": "Individual micro food-processing units may receive 35% credit-linked capital subsidy up to ₹10 lakh, subject to eligibility and guidelines.",
        "why": "A strong match for spice processing, pickles, snacks, flour, local food products and value-added agricultural produce.",
        "source": "Ministry of Food Processing Industries"
    },
    {
        "name": "Kisan Credit Card (KCC)",
        "best_for": "Farmers and eligible agricultural/allied activities.",
        "description": "Provides formal credit access for agricultural and allied working-capital needs, subject to lending and eligibility conditions.",
        "key": "Can support eligible crop and allied agricultural credit requirements through participating financial institutions.",
        "why": "Useful when the main business is farming or an eligible allied agricultural activity.",
        "source": "Government of India / Department of Financial Services"
    },
    {
        "name": "Agriculture Infrastructure Fund (AIF)",
        "best_for": "Post-harvest infrastructure and eligible community farming assets.",
        "description": "Provides financing support for eligible agriculture infrastructure such as post-harvest management and community farming assets.",
        "key": "Eligible loans can receive interest subvention of 3% per year on the loan component up to ₹2 crore, subject to scheme conditions.",
        "why": "Useful for storage, grading, primary processing and other eligible agricultural infrastructure.",
        "source": "Department of Agriculture & Farmers Welfare"
    },
    {
        "name": "Agri-Clinics and Agri-Business Centres (ACABC)",
        "best_for": "Eligible agriculture-trained entrepreneurs providing farm-related services.",
        "description": "Supports trained agricultural professionals/eligible candidates in setting up agri-clinics and agri-business centres that provide advisory and agricultural services to farmers.",
        "key": "Eligibility, training, project cost and subsidy provisions depend on the current ACABC guidelines.",
        "why": "Useful for agriculture advisory, farm services, input-related services and other eligible agri-business models.",
        "source": "MANAGE / Ministry of Agriculture & Farmers Welfare"
    },
    {
        "name": "DAY-NRLM – Deendayal Antyodaya Yojana",
        "best_for": "Rural women-led Self Help Groups and rural livelihoods.",
        "description": "A rural livelihoods programme that works through Self Help Groups and community institutions to improve access to finance, skills, enterprise support and sustainable livelihoods.",
        "key": "Support is delivered through the rural livelihood mission structure and applicable state-level mechanisms.",
        "why": "Useful for group enterprises, food processing, handicrafts and other SHG-based rural businesses.",
        "source": "Ministry of Rural Development"
    },
    {
        "name": "PM Vishwakarma",
        "best_for": "Eligible traditional artisans and craftspeople.",
        "description": "Supports eligible traditional artisans and craftspeople with recognition, skill development, toolkit support, credit and market-oriented assistance under the scheme.",
        "key": "Benefits and eligible trades are subject to the official scheme guidelines.",
        "why": "Relevant to tailoring and eligible traditional craft/artisan businesses.",
        "source": "Government of India"
    },
    {
        "name": "PM-KUSUM",
        "best_for": "Eligible farmers and agricultural energy/solar applications.",
        "description": "Supports solar-energy-related interventions in agriculture, including eligible solar pumps and other components under the scheme.",
        "key": "Component, subsidy and implementation conditions vary and are administered through the relevant authorities.",
        "why": "Relevant where reliable agricultural energy and irrigation are important to the business model.",
        "source": "Ministry of New and Renewable Energy"
    }
]

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def money(value):
    return f"₹{value:,.0f}"

def calculate_match(business, capital, resource, interest, water, experience, location, resources_list=None):
    score = 0
    reasons = []
    resources_list = resources_list or []

    low, high = business["capital"]

    # Capital fit
    if capital >= high:
        score += 30
        reasons.append("Your available capital comfortably covers the indicative investment range.")
    elif capital >= low:
        score += 25
        reasons.append("Your capital fits the lower-to-middle part of the indicative investment range.")
    elif capital >= low * 0.5:
        score += 12
        reasons.append("Your capital is below the typical starting range, so a smaller pilot may be needed.")
    else:
        score += 3
        reasons.append("Capital is currently limited for this model.")

    # Resource fit
    resource_lower = resource.lower()
    resource_matches = [r.lower() for r in business["resources"]]
    if any(r in resource_lower for r in resource_matches) or resource == "Not sure / I have limited resources":
        score += 20
        reasons.append("Your available resources can support this type of business.")
    else:
        score += 7
        reasons.append("You may need to arrange some additional resources before starting.")

    # Interest fit
    interest_lower = interest.lower()
    if any(x.lower() in interest_lower for x in business["interests"]):
        score += 20
        reasons.append("The business matches your stated interest.")
    else:
        score += 7

    # Water fit
    if "Water" in business["resources"] or "water" in business["name"].lower():
        if water == "Good":
            score += 10
            reasons.append("Good water availability improves feasibility.")
        elif water == "Limited":
            score += 4
            reasons.append("Limited water availability makes this business more sensitive to planning.")
        else:
            score += 1
    else:
        score += 8

    # Experience
    if experience == "Some experience":
        score += 10
        reasons.append("Your existing experience reduces the learning curve.")
    elif experience == "Experienced":
        score += 10
        reasons.append("Your experience is a strong fit for execution.")
    else:
        score += 5
        reasons.append("A small pilot and basic training are recommended before scaling.")

    # Location
    if location in business["locations"]:
        score += 10
        reasons.append(f"{location} is included in the prototype's suitable-location profile.")
    else:
        score += 5

    # Detailed resource specifications (Feature 4): land area, water, labour
    # and market access from the user's added resource entries give a small
    # additional adjustment on top of the basic inputs above.
    if resources_list:
        total_land = sum(float(r.get("land_area") or 0) for r in resources_list)
        total_labor = sum(float(r.get("labor") or 0) for r in resources_list)
        best_market = "Poor"
        market_rank = {"Poor": 0, "Moderate": 1, "Good": 2}
        for r in resources_list:
            m = r.get("market_access", "Poor")
            if market_rank.get(m, 0) > market_rank.get(best_market, 0):
                best_market = m

        needs_land = "Land" in business["resources"]
        if needs_land:
            if total_land >= 1:
                score += 6
                reasons.append("Your recorded land area supports this business.")
            elif total_land > 0:
                score += 3
            # else: no bonus, no penalty (kept neutral for non-land businesses too)

        if total_labor >= 2:
            score += 4
        elif total_labor >= 1:
            score += 2

        if best_market == "Good":
            score += 5
            reasons.append("Good recorded market access improves feasibility.")
        elif best_market == "Moderate":
            score += 2

    return min(score, 100), reasons


def compute_investment_estimate(business, investment):
    """Feature 7: given a planned investment amount, return an indicative
    annual benefit range and the typical timeline, using this prototype's
    demonstration success-rate/return assumptions for the business."""
    low_ret, high_ret = business["expected_return_pct"]
    benefit_low = investment * (low_ret / 100)
    benefit_high = investment * (high_ret / 100)
    t_low, t_high = business["timeline_months"]
    return benefit_low, benefit_high, t_low, t_high


def scheme_for_business(business):
    return business["schemes"]




# ============================================================
# ENHANCED HYPER-LOCAL ADVISORY DATA + FINANCIAL ENGINE
# ============================================================
# These are structured prototype assumptions. Where official
# information is unavailable, the UI explicitly labels estimates/fallbacks.
LOCATION_CONTEXT = {
    "Hubballi": {"state":"Karnataka","district":"Dharwad","climate":"Semi-arid","temperature_c":26,"rainfall_mm":700,"soil":"Red/black mixed","water":"Medium","market_access":"Good"},
    "Dharwad": {"state":"Karnataka","district":"Dharwad","climate":"Semi-arid","temperature_c":25,"rainfall_mm":750,"soil":"Black/red mixed","water":"Medium","market_access":"Good"},
    "Belagavi": {"state":"Karnataka","district":"Belagavi","climate":"Moderate","temperature_c":24,"rainfall_mm":900,"soil":"Red/black","water":"Medium","market_access":"Good"},
    "Bengaluru": {"state":"Karnataka","district":"Bengaluru Urban","climate":"Moderate","temperature_c":23,"rainfall_mm":900,"soil":"Red loam","water":"Medium","market_access":"Good"},
    "Mysuru": {"state":"Karnataka","district":"Mysuru","climate":"Moderate","temperature_c":24,"rainfall_mm":800,"soil":"Red loam","water":"Medium","market_access":"Good"},
    "Shivamogga": {"state":"Karnataka","district":"Shivamogga","climate":"Humid","temperature_c":24,"rainfall_mm":1800,"soil":"Red loam","water":"High","market_access":"Good"},
    "Davanagere": {"state":"Karnataka","district":"Davanagere","climate":"Semi-arid","temperature_c":26,"rainfall_mm":650,"soil":"Black soil","water":"Medium","market_access":"Good"},
    "Gadag": {"state":"Karnataka","district":"Gadag","climate":"Semi-arid","temperature_c":27,"rainfall_mm":600,"soil":"Black soil","water":"Limited","market_access":"Moderate"},
    "Haveri": {"state":"Karnataka","district":"Haveri","climate":"Moderate","temperature_c":25,"rainfall_mm":750,"soil":"Black/red","water":"Medium","market_access":"Good"},
    "Vijayapura": {"state":"Karnataka","district":"Vijayapura","climate":"Dry","temperature_c":27,"rainfall_mm":550,"soil":"Black soil","water":"Limited","market_access":"Moderate"},
    "Kalaburagi": {"state":"Karnataka","district":"Kalaburagi","climate":"Dry","temperature_c":28,"rainfall_mm":650,"soil":"Deep black soil","water":"Limited","market_access":"Moderate"},
    "Raichur": {"state":"Karnataka","district":"Raichur","climate":"Dry","temperature_c":28,"rainfall_mm":650,"soil":"Black/alluvial","water":"Medium","market_access":"Good"},
    "Tumakuru": {"state":"Karnataka","district":"Tumakuru","climate":"Semi-arid","temperature_c":25,"rainfall_mm":700,"soil":"Red loam","water":"Limited","market_access":"Good"},
    "Chitradurga": {"state":"Karnataka","district":"Chitradurga","climate":"Dry","temperature_c":26,"rainfall_mm":600,"soil":"Red/black","water":"Limited","market_access":"Moderate"},
}

# ------------------------------------------------------------
# LOCATION-AWARE TEMPERATURE ENGINE
# ------------------------------------------------------------
@st.cache_data(ttl=1800, show_spinner=False)
def get_location_temperature(location):
    """Get temperature from the selected location, with a safe fallback."""
    fallback = LOCATION_CONTEXT.get(location, {}).get("temperature_c")
    if fallback is None:
        fallback = 25.0
    if requests is None or not location:
        return float(fallback), "Location planning profile"
    try:
        geo = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": str(location), "count": 1, "language": "en", "format": "json", "countryCode": "IN"},
            timeout=5,
        )
        geo.raise_for_status()
        results = geo.json().get("results", [])
        if not results:
            return float(fallback), "Location planning profile"
        lat, lon = results[0].get("latitude"), results[0].get("longitude")
        if lat is None or lon is None:
            return float(fallback), "Location planning profile"
        weather = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": lat, "longitude": lon, "current": "temperature_2m", "timezone": "auto"},
            timeout=5,
        )
        weather.raise_for_status()
        temp = weather.json().get("current", {}).get("temperature_2m")
        if temp is None:
            return float(fallback), "Location planning profile"
        return float(temp), "Live location weather"
    except Exception:
        return float(fallback), "Location planning profile"

# Indicative crop profiles. Existing CROP_DATA remains the source for
# displayed demo prices; these fields are planning assumptions, not official
# agronomic guarantees.
CROP_PROFILES = {
    "Maize":{"water":"Medium","duration":"90–120 days","yield":"2.5–4.5 t/ha","soil":"Well-drained loam/black soil"},
    "Groundnut":{"water":"Low–Medium","duration":"100–120 days","yield":"1.2–2.0 t/ha","soil":"Sandy/red/loam"},
    "Cotton":{"water":"Medium","duration":"150–180 days","yield":"1.5–2.5 t/ha","soil":"Black soil"},
    "Tur":{"water":"Low–Medium","duration":"150–180 days","yield":"0.8–1.5 t/ha","soil":"Well-drained black/red soil"},
    "Bengal Gram":{"water":"Low","duration":"100–120 days","yield":"0.8–1.5 t/ha","soil":"Black/loam"},
    "Jowar":{"water":"Low","duration":"100–120 days","yield":"1.5–2.5 t/ha","soil":"Black/red soil"},
    "Bajra":{"water":"Low","duration":"75–100 days","yield":"1.5–2.5 t/ha","soil":"Light, well-drained soil"},
    "Sunflower":{"water":"Low–Medium","duration":"90–110 days","yield":"0.7–1.2 t/ha","soil":"Well-drained soil"},
    "Soybean":{"water":"Medium","duration":"90–120 days","yield":"1.5–2.5 t/ha","soil":"Well-drained loam/black soil"},
    "Rice":{"water":"High","duration":"110–150 days","yield":"3–5 t/ha","soil":"Clay/loam with water retention"},
    "Ragi":{"water":"Low–Medium","duration":"100–120 days","yield":"1.5–2.5 t/ha","soil":"Red loam"},
    "Sugarcane":{"water":"High","duration":"10–14 months","yield":"70–100 t/ha","soil":"Deep fertile soil"},
    "Tomato":{"water":"Medium–High","duration":"90–140 days","yield":"25–50 t/ha","soil":"Well-drained loam"},
    "Onion":{"water":"Medium","duration":"100–150 days","yield":"20–35 t/ha","soil":"Well-drained loam"},
    "Chilli":{"water":"Medium","duration":"120–180 days","yield":"1.5–3.0 t/ha dry","soil":"Well-drained loam"},
    "Turmeric":{"water":"Medium–High","duration":"7–9 months","yield":"20–30 t/ha fresh","soil":"Loam"},
    "Beans":{"water":"Medium","duration":"60–90 days","yield":"8–15 t/ha","soil":"Well-drained loam"},
    "Cabbage":{"water":"Medium","duration":"80–120 days","yield":"25–45 t/ha","soil":"Fertile loam"},
    "Potato":{"water":"Medium","duration":"80–120 days","yield":"20–35 t/ha","soil":"Sandy loam"},
    "Coconut":{"water":"Medium–High","duration":"Perennial","yield":"Indicative: 60–100 nuts/tree/year","soil":"Well-drained loam"},
    "Banana":{"water":"High","duration":"10–14 months","yield":"30–50 t/ha","soil":"Deep fertile loam"},
    "Ginger":{"water":"Medium–High","duration":"7–9 months","yield":"12–20 t/ha","soil":"Loose loam"},
    "Pumpkin":{"water":"Medium","duration":"90–120 days","yield":"15–30 t/ha","soil":"Loam"},
    "Bottle Gourd":{"water":"Medium","duration":"90–120 days","yield":"15–25 t/ha","soil":"Loam"},
    "Cucumber":{"water":"Medium","duration":"60–90 days","yield":"10–20 t/ha","soil":"Sandy loam"},
    "Coriander":{"water":"Low–Medium","duration":"40–90 days","yield":"Indicative; depends on leaf/seed production","soil":"Well-drained loam"},
    "Spinach":{"water":"Medium","duration":"30–60 days","yield":"Indicative; repeated harvest possible","soil":"Fertile loam"},
    "Carrot":{"water":"Medium","duration":"70–100 days","yield":"20–35 t/ha","soil":"Loose sandy loam"},
    "Cauliflower":{"water":"Medium","duration":"90–150 days","yield":"20–35 t/ha","soil":"Fertile loam"},
    "Capsicum":{"water":"Medium","duration":"120–180 days","yield":"15–30 t/ha","soil":"Well-drained loam"},
    "Beetroot":{"water":"Medium","duration":"60–90 days","yield":"15–25 t/ha","soil":"Sandy loam"},
    "Radish":{"water":"Medium","duration":"35–60 days","yield":"15–25 t/ha","soil":"Loose sandy loam"},
    "Papaya":{"water":"Medium–High","duration":"9–12 months to first harvest","yield":"Indicative; varies widely","soil":"Well-drained fertile soil"},
    "Guava":{"water":"Medium","duration":"2–3 years to meaningful harvest","yield":"Indicative; varies by cultivar","soil":"Well-drained soil"},
    "Green Gram":{"water":"Low","duration":"60–75 days","yield":"0.6–1.0 t/ha","soil":"Well-drained loam"},
    "Black Gram":{"water":"Low","duration":"70–90 days","yield":"0.6–1.0 t/ha","soil":"Well-drained loam"},
    "Fenugreek Leaves":{"water":"Low–Medium","duration":"30–50 days","yield":"Indicative; repeated harvest possible","soil":"Loam"},
    "Lady Finger":{"water":"Medium","duration":"50–80 days","yield":"8–15 t/ha","soil":"Loam"},
    "Pomegranate":{"water":"Medium","duration":"18–24 months to commercial harvest","yield":"Indicative; varies widely","soil":"Well-drained soil"},
    "Grapes":{"water":"Medium–High","duration":"18–24 months to commercial harvest","yield":"Indicative; varies by cultivar and trellis system","soil":"Well-drained loam"},
    "Orange":{"water":"Medium","duration":"3–4 years to meaningful harvest","yield":"Indicative; varies by cultivar","soil":"Well-drained loam"},
}

def _secret(name, default=""):
    try:
        return st.secrets.get(name, default)
    except Exception:
        return default

def resource_totals(resources):
    totals = {"land":0.0,"water":"None","labor":0,"market":"Poor","shop":0,"vehicle":0,"storage":0,"electricity":0,"internet":0}
    water_rank = {"None":0,"Low":1,"Medium":2,"High":3}
    market_rank = {"Poor":0,"Moderate":1,"Good":2}
    for r in resources or []:
        typ = str(r.get("type",""))
        if typ == "Land":
            totals["land"] += float(r.get("land_area",0) or 0)
        if typ == "Labour":
            totals["labor"] += int(r.get("labor",0) or 0)
        if typ == "Shop space":
            totals["shop"] += 1
        if typ == "Vehicle":
            totals["vehicle"] += 1
        if typ == "Storage":
            totals["storage"] += 1
        if typ == "Electricity":
            totals["electricity"] += 1
        if typ == "Internet":
            totals["internet"] += 1
        w = str(r.get("water","None"))
        if water_rank.get(w,0) > water_rank.get(totals["water"],0):
            totals["water"] = w
        m = str(r.get("market_access","Poor"))
        if market_rank.get(m,0) > market_rank.get(totals["market"],0):
            totals["market"] = m
    return totals

def business_financial_model(business):
    """Build a transparent small-scale model from existing business ranges.
    All outputs are labelled estimates and use ranges, not guarantees."""
    low, high = business["capital"]
    recommended = int((low + high) / 2)
    maximum = high
    # Conservative assumptions vary by business type.
    low_ret, high_ret = business.get("expected_return_pct",(10,25))
    monthly_revenue_low = low * (1 + low_ret/100) / 12
    monthly_revenue_high = recommended * (1 + high_ret/100) / 8
    # Cost is kept separate from revenue; benefit is revenue minus operating cost.
    cost_ratio_low, cost_ratio_high = 0.55, 0.75
    monthly_cost_low = monthly_revenue_low * cost_ratio_low
    monthly_cost_high = monthly_revenue_high * cost_ratio_high
    return {
        "minimum_investment": low,
        "recommended_investment": recommended,
        "maximum_investment": maximum,
        "monthly_revenue": (monthly_revenue_low, monthly_revenue_high),
        "monthly_cost": (monthly_cost_low, monthly_cost_high),
        "monthly_benefit": (max(0, monthly_revenue_low-monthly_cost_high), max(0, monthly_revenue_high-monthly_cost_low)),
        "roi": (max(0, low_ret*0.5), max(0, high_ret)),
    }

def financial_projection(business, investment):
    fm = business_financial_model(business)
    min_i = fm["minimum_investment"]
    low_ret, high_ret = business.get("expected_return_pct",(10,25))
    scale = max(0.35, min(1.75, investment / max(min_i,1)))
    rev_low, rev_high = fm["monthly_revenue"]
    cost_low, cost_high = fm["monthly_cost"]
    rev_low *= scale; rev_high *= scale
    cost_low *= scale; cost_high *= scale
    benefit_low = max(0, rev_low-cost_high)
    benefit_high = max(0, rev_high-cost_low)
    annual_low, annual_high = benefit_low*12, benefit_high*12
    roi_low = (annual_low / investment * 100) if investment else 0
    roi_high = (annual_high / investment * 100) if investment else 0
    break_low = investment/benefit_high if benefit_high else float("inf")
    break_high = investment/benefit_low if benefit_low else float("inf")
    return {
        "revenue":(rev_low,rev_high),"cost":(cost_low,cost_high),
        "benefit":(benefit_low,benefit_high),
        "annual_benefit":(annual_low,annual_high),
        "roi":(roi_low,roi_high),
        "break_even":(break_low,break_high)
    }

def calculate_enhanced_match(business, capital, resource, interest, water, experience, location, resources):
    base_score, reasons = calculate_match(business, capital, resource, interest, water, experience, location, resources)
    totals = resource_totals(resources)
    ctx = LOCATION_CONTEXT.get(location, {"state":"Karnataka","district":"Locality profile pending","climate":"Use supplied climate input","temperature_c":"Not available","rainfall_mm":"Not available","soil":"Use supplied soil input","water":"Use supplied water input","market_access":"Use supplied market access input"})
    score = float(base_score)
    required = " ".join(business.get("resources",[])).lower()
    # Resource-specific scoring
    if "land" in required:
        score += 6 if totals["land"] >= 1 else (-4 if resources else 0)
    if "vehicle" in required:
        score += 6 if totals["vehicle"] else -3
    if "shop" in required or "workspace" in required:
        score += 5 if totals["shop"] or any("workspace" in str(r.get("type","")).lower() for r in resources) else 0
    if totals["labor"]:
        score += min(5, totals["labor"])
    # Water + local climate + market access
    if ("water" in required or business.get("is_crop_based")):
        wr = {"None":0,"Low":1,"Medium":2,"High":3}.get(totals["water"],0)
        if water == "Good": wr += 1
        elif water == "Limited": wr -= 0.5
        score += max(-5,min(5,wr))
    if ctx.get("market_access") == "Good":
        score += 3
    # Crop suitability: crop-based businesses must have local crops.
    if business.get("is_crop_based") and not suitable_crops_for_location(location):
        score -= 10
    return max(0,min(100,round(score))), reasons, totals

def dynamic_success_rate(business, match_score, capital, resources, location):
    totals = resource_totals(resources)
    fm = business_financial_model(business)
    risk_penalty = 0
    if business.get("risks"):
        high_risks = sum(1 for r in business["risks"] if str(r.get("likelihood","")).lower()=="high")
        risk_penalty += min(12, high_risks*4)
    capital_factor = 1 if capital >= fm["minimum_investment"] else 0.75
    resource_factor = 1 if resources else 0.9
    rate = match_score*0.55 + business.get("success_rate",60)*0.25 + 20*capital_factor*resource_factor - risk_penalty
    return int(max(20,min(95,round(rate))))

def crop_analysis_rows(location):
    rows=[]
    for crop in suitable_crops_for_location(location):
        profile=CROP_PROFILES.get(crop,{})
        market = CROP_DATA.get(crop, {})
        rows.append({
            "crop":crop,"why":f"Listed as suitable for {location} in the prototype location profile.",
            "climate":LOCATION_CONTEXT.get(location,{"climate":"Use supplied climate input"}).get("climate","Use supplied climate input"),
            "water":profile.get("water","Not available"),
            "duration":profile.get("duration","Not available"),
            "yield":profile.get("yield","Not available"),
            "soil":profile.get("soil","Not available"),
            "price":market.get("price",0),
            "unit":market.get("unit","as reported"),
        })
    return rows

def ensure_business_fields():
    for b in BUSINESSES:
        fm=business_financial_model(b)
        b.setdefault("minimum_investment",fm["minimum_investment"])
        b.setdefault("recommended_investment",fm["recommended_investment"])
        b.setdefault("maximum_investment",fm["maximum_investment"])
        b.setdefault("financial_model",fm)
        b.setdefault("required_resources",b.get("resources",[]))
        b.setdefault("location_suitability",b.get("locations",[]))
        b.setdefault("climate_requirements","Depends on the specific activity; compare with local profile.")
        b.setdefault("water_requirements","Depends on the activity and scale.")
        b.setdefault("labour_requirements","Depends on the operating scale.")
        b.setdefault("market_requirements","Local demand and access to a selling channel are required.")
ensure_business_fields()

# ============================================================
# LOCATION HELPERS — defined before all callers
# ============================================================
def automatic_location_water(location):
    """Return the configured planning water level for the selected location."""
    return str(LOCATION_CONTEXT.get(location, {}).get("water", "Medium"))

def automatic_location_irrigation(location):
    return {"High":"Reliable","Medium":"Available","Limited":"Limited","Low":"Limited","None":"Rain-fed"}.get(automatic_location_water(location), "Limited")

def automatic_location_season(location=None, today=None):
    """Return the automatically selected agricultural season for the state/UT."""
    state = str(location or "").strip()
    month = (today or datetime.date.today()).month
    if state == "Tamil Nadu":
        if month in (10, 11, 12, 1): return "Kharif"
        if month in (2, 3, 4, 5): return "Rabi"
        return "Summer"
    if state in {"Kerala", "Goa", "Andaman and Nicobar Islands", "Lakshadweep"}:
        if month in (6, 7, 8, 9, 10, 11): return "Kharif"
        if month in (12, 1, 2, 3): return "Rabi"
        return "Summer"
    if state in {"Assam", "Arunachal Pradesh", "Meghalaya", "Manipur", "Mizoram", "Nagaland", "Tripura"}:
        if month in (4, 5, 6, 7, 8, 9, 10): return "Kharif"
        if month in (11, 12, 1, 2, 3): return "Rabi"
        return "Summer"
    if month in (6, 7, 8, 9, 10): return "Kharif"
    if month in (11, 12, 1, 2): return "Rabi"
    return "Summer"

@st.cache_data(show_spinner=False)
def _npk_location_reference(location):
    """Average N/P/K/pH/humidity readings for the crops the location profile
    already recommends, pulled straight from the uploaded NPK dataset
    (Crop_recommendation.csv). Falls back to the dataset-wide average, and
    finally to safe planning defaults, so Step 2 always has a sensible value
    even when a location has no exact crop match in the file."""
    defaults = {"N": 70.0, "P": 40.0, "K": 40.0, "soil_ph": 6.5, "humidity": 70.0}
    df, source = load_npk_reference()
    if df is None:
        return defaults, source
    crop_names = CROP_LOCATION_SUITABILITY.get(location, []) or AGRI_LOCATION_CROPS.get(location, [])
    canon_targets = {_canonical_crop(c) for c in crop_names}
    labels_canon = df["label"].apply(_canonical_crop)
    sub = df[labels_canon.isin(canon_targets)]
    if sub.empty:
        sub = df  # dataset-wide average as a broader fallback
    if sub.empty:
        return defaults, source
    result = {
        "N": round(float(sub["n"].mean()), 1),
        "P": round(float(sub["p"].mean()), 1),
        "K": round(float(sub["k"].mean()), 1),
        "soil_ph": round(float(sub["ph"].mean()), 2),
        "humidity": round(float(sub["humidity"].mean()), 1),
        "rainfall": round(float(sub["rainfall"].mean()), 1),
    }
    return result, source

def automatic_location_rainfall(location):
    """Rainfall (mm) for the selected location: the curated location profile
    when available, otherwise the average rainfall of the uploaded NPK
    dataset for the crops mapped to that location."""
    ctx_rain = LOCATION_CONTEXT.get(location, {}).get("rainfall_mm")
    if isinstance(ctx_rain, (int, float)):
        return float(ctx_rain)
    npk_vals, _ = _npk_location_reference(location)
    return float(npk_vals.get("rainfall", 700.0))

def automatic_location_soil_npk(location):
    """Public helper used by Step 2: N, P, K, soil pH, humidity and rainfall
    derived automatically from the uploaded NPK/soil dataset for the crops
    mapped to this location (falling back to the curated location profile
    for rainfall where that is more specific). Temperature keeps using its
    existing live-weather / location-profile source."""
    values, source = _npk_location_reference(location)
    values["rainfall"] = automatic_location_rainfall(location)
    return values, source

# ============================================================
# GRAM VAANI — MULTILINGUAL VOICE ASSISTANT
# ============================================================
_GS_VOICE_TEMPLATE = r'''
<!doctype html>
<html><head><meta charset="utf-8">
<meta name="referrer" content="no-referrer">
<style>
*{box-sizing:border-box}body{margin:0;font-family:Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans Kannada","Noto Sans Devanagari",sans-serif;background:linear-gradient(135deg,#0d3b18,#1f6b2a 55%,#e8f5e9);color:#fff}
.wrap{padding:18px 20px 16px;position:relative;overflow:hidden}
.glow{position:absolute;width:190px;height:190px;border-radius:50%;background:rgba(255,255,255,.08);right:-45px;top:-70px}
.top{display:flex;justify-content:space-between;gap:14px;align-items:center;position:relative;z-index:1}
.brand{display:flex;gap:12px;align-items:center}
.logo{width:48px;height:48px;border-radius:15px;background:rgba(255,255,255,.15);display:flex;align-items:center;justify-content:center;font-size:26px;box-shadow:0 8px 22px rgba(0,0,0,.15)}
.kicker{font-size:11px;letter-spacing:.13em;text-transform:uppercase;opacity:.8;font-weight:800}
h1{font-size:22px;margin:2px 0 0;font-weight:850;line-height:1.25}
.badge{padding:7px 10px;border-radius:999px;background:rgba(255,255,255,.13);font-size:11px;font-weight:750;white-space:nowrap}
.controls{display:grid;grid-template-columns:1.05fr 1.15fr 1fr .7fr;gap:9px;margin-top:15px;position:relative;z-index:1}
button,select{border:1px solid rgba(255,255,255,.22);border-radius:11px;padding:10px 11px;background:rgba(255,255,255,.12);color:#fff;font-weight:750;font-size:12px;cursor:pointer;outline:none;font-family:inherit}
select option{color:#123;background:#fff}
button:hover{background:rgba(255,255,255,.2)}
.mic{background:#fff;color:#176323;border:none;font-size:13px}
.mic:hover{background:#f1f8f2}
.mic.listening{background:#ffebee;color:#b71c1c;animation:pulse 1.1s infinite}
@keyframes pulse{50%{transform:scale(1.03);box-shadow:0 0 0 7px rgba(255,255,255,.12)}}
.ask{display:flex;gap:8px;margin-top:10px;position:relative;z-index:1}
input{flex:1;border:1px solid rgba(255,255,255,.22);border-radius:11px;padding:11px 12px;background:rgba(255,255,255,.12);color:#fff;font-size:13px;outline:none;font-family:inherit}
input::placeholder{color:rgba(255,255,255,.68)}
.answer{margin-top:11px;background:#fff;color:#243127;border-radius:14px;padding:13px 14px;min-height:68px;max-height:150px;overflow:auto;box-shadow:0 8px 20px rgba(0,0,0,.12);line-height:1.55;font-size:13px;position:relative;z-index:1}
.answer b{color:#1b5e20}
.quick{display:flex;gap:7px;flex-wrap:wrap;margin-top:9px;position:relative;z-index:1}
.quick button{font-size:11px;padding:7px 9px;background:rgba(255,255,255,.1)}
.status{font-size:11px;opacity:.85;margin-top:8px;position:relative;z-index:1;min-height:14px}
@media(max-width:650px){.controls{grid-template-columns:1fr 1fr}.badge{display:none}}
</style></head>
<body><div class="wrap"><div class="glow"></div>
<div class="top"><div class="brand"><div class="logo">🎙️</div><div><div class="kicker" id="kicker"></div><h1 id="title"></h1></div></div><div class="badge">EN • HI • KN</div></div>
<div class="controls">
<select id="lang" aria-label="Language"><option value="en-IN">English</option><option value="hi-IN">हिन्दी</option><option value="kn-IN">ಕನ್ನಡ</option></select>
<button class="mic" id="mic"></button>
<button id="speak"></button>
<button id="stop"></button>
</div>
<div class="ask"><input id="q"><button id="ask"></button></div>
<div class="quick" id="quick"></div>
<div class="answer" id="answer"></div>
<div class="status" id="status"></div>
</div>
<script>
const C = __CONTEXT__;
const UI = __UI__;
const A={
'en-IN':{hello:'Hello! I am Gram Vaani, your multilingual farm and rural-business assistant.',how:'Gram Sahayak starts with one shared location, then connects crop information, market prices, government schemes, financial guidance and business recommendations. The Business page follows Select Business, Enter Inputs, then Strategic Output.',temp:()=>`At ${C.context.location}, the location temperature is about ${C.context.temperature} degrees Celsius. Source: ${C.context.temperatureSource}.`,loc:()=>`Your selected location is ${C.context.location}. Its planning water profile is ${C.context.water} and the mapped rainfall value is ${C.context.rainfall} millimetres.`,business:'Business Recommendation compares practical inputs such as resources, capital, market access and location context. It then gives an execution roadmap, risk controls, financial benchmarks and related schemes.',scheme:'Government scheme information is grouped by activity. Examples include KCC for eligible agricultural credit, AIF for eligible agricultural infrastructure, MIDH and NHB for eligible horticulture components, NLM for specified livestock entrepreneurship, FIDF for eligible fisheries infrastructure, PMFME for eligible micro food processing, and MUDRA or PMEGP for eligible micro-enterprise finance. Always verify current official guidelines.',market:'Market Prices is designed to show the latest available mandi information for the selected location when the official data source is available. Compare market, quality, transport and buyer deductions before making a sale decision.',finance:'Financial Assistant provides planning calculations such as EMI, affordability and cash-flow views. These are estimates; actual loan terms depend on the lender and the approved application.',npk:'NPK means Nitrogen, Phosphorus and Potassium. Gram Sahayak can use these soil values with pH, humidity, rainfall and temperature in its crop-environment matching layer when the required reference data is available.'},
'hi-IN':{hello:'नमस्ते! मैं ग्राम वाणी हूँ, आपका बहुभाषी कृषि और ग्रामीण व्यवसाय सहायक।',how:'ग्राम सहायक में पहले एक साझा स्थान चुना जाता है। इसके बाद फसल जानकारी, मंडी भाव, सरकारी योजनाएँ, वित्तीय सहायता और व्यवसाय सिफारिशें आपस में जुड़ती हैं। व्यवसाय पेज में तीन चरण हैं: व्यवसाय चुनें, जानकारी भरें और रणनीतिक परिणाम देखें।',temp:()=>`आपके स्थान ${C.context.location} में स्थान-आधारित तापमान लगभग ${C.context.temperature} डिग्री सेल्सियस है। स्रोत: ${C.context.temperatureSource}।`,loc:()=>`आपका चुना हुआ स्थान ${C.context.location} है। यहाँ नियोजन के लिए पानी की स्थिति ${C.context.water} और मैप किया गया वर्षा मान ${C.context.rainfall} मिलीमीटर है।`,business:'व्यवसाय सिफारिश में स्थान, संसाधन, पूंजी और बाजार जैसे इनपुट देखकर नियम-आधारित आकलन किया जाता है। इसके बाद रोडमैप, जोखिम नियंत्रण, वित्तीय बेंचमार्क और संबंधित योजनाएँ दिखाई जाती हैं।',scheme:'योजनाएँ गतिविधि के अनुसार दिखाई जाती हैं। उदाहरण के लिए पात्र कृषि ऋण के लिए KCC, पात्र कृषि अवसंरचना के लिए AIF, बागवानी के लिए MIDH और NHB के संबंधित घटक, पशुपालन के लिए NLM, मत्स्य अवसंरचना के लिए FIDF, खाद्य प्रसंस्करण के लिए PMFME और पात्र सूक्ष्म उद्यमों के लिए MUDRA या PMEGP शामिल हो सकते हैं। वर्तमान आधिकारिक नियम अवश्य जाँचें।',market:'मार्केट प्राइस पेज उपलब्ध होने पर चयनित स्थान के लिए नवीनतम मंडी जानकारी दिखाने के लिए बनाया गया है। बिक्री से पहले बाजार, गुणवत्ता, परिवहन और खरीदार की कटौती की तुलना करें।',finance:'फाइनेंशियल असिस्टेंट EMI, वहनीयता और कैश-फ्लो जैसी योजना गणनाएँ देता है। वास्तविक ऋण शर्तें बैंक और स्वीकृत आवेदन पर निर्भर करती हैं।',npk:'NPK का अर्थ नाइट्रोजन, फॉस्फोरस और पोटैशियम है। जहाँ संदर्भ डेटा उपलब्ध है, ग्राम सहायक इन मानों को pH, आर्द्रता, वर्षा और तापमान के साथ फसल मिलान में उपयोग कर सकता है।'},
'kn-IN':{hello:'ನಮಸ್ಕಾರ! ನಾನು ಗ್ರಾಮ ವಾಣಿ. ನಿಮ್ಮ ಬಹುಭಾಷಾ ಕೃಷಿ ಮತ್ತು ಗ್ರಾಮೀಣ ವ್ಯವಹಾರ ಸಹಾಯಕ.',how:'ಗ್ರಾಮ ಸಹಾಯಕದಲ್ಲಿ ಮೊದಲು ಒಂದು ಸ್ಥಳವನ್ನು ಆಯ್ಕೆ ಮಾಡಲಾಗುತ್ತದೆ. ನಂತರ ಬೆಳೆ ಮಾಹಿತಿ, ಮಾರುಕಟ್ಟೆ ಬೆಲೆ, ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು, ಹಣಕಾಸು ಮಾರ್ಗದರ್ಶನ ಮತ್ತು ವ್ಯವಹಾರ ಶಿಫಾರಸುಗಳು ಸಂಪರ್ಕಗೊಳ್ಳುತ್ತವೆ. ವ್ಯವಹಾರ ಪುಟದಲ್ಲಿ ಮೂರು ಹಂತಗಳಿವೆ: ವ್ಯವಹಾರ ಆಯ್ಕೆ, ಮಾಹಿತಿ ನಮೂದು ಮತ್ತು ತಂತ್ರಾತ್ಮಕ ಫಲಿತಾಂಶ.',temp:()=>`ನಿಮ್ಮ ಸ್ಥಳ ${C.context.location} ನಲ್ಲಿ ಸ್ಥಳಾಧಾರಿತ ತಾಪಮಾನ ಸುಮಾರು ${C.context.temperature} ಡಿಗ್ರಿ ಸೆಲ್ಸಿಯಸ್ ಇದೆ. ಮೂಲ: ${C.context.temperatureSource}.`,loc:()=>`ನೀವು ಆಯ್ಕೆ ಮಾಡಿದ ಸ್ಥಳ ${C.context.location}. ಯೋಜನಾ ನೀರಿನ ಸ್ಥಿತಿ ${C.context.water} ಮತ್ತು ಮ್ಯಾಪ್ ಮಾಡಲಾದ ಮಳೆಯ ಪ್ರಮಾಣ ${C.context.rainfall} ಮಿಲಿಮೀಟರ್.`,business:'ವ್ಯವಹಾರ ಶಿಫಾರಸು ಸ್ಥಳ, ಸಂಪನ್ಮೂಲ, ಬಂಡವಾಳ ಮತ್ತು ಮಾರುಕಟ್ಟೆ ಮಾಹಿತಿಯನ್ನು ಬಳಸಿ ನಿಯಮಾಧಾರಿತ ಮೌಲ್ಯಮಾಪನ ಮಾಡುತ್ತದೆ. ನಂತರ ಕಾರ್ಯಯೋಜನೆ, ಅಪಾಯ ನಿಯಂತ್ರಣ, ಹಣಕಾಸು ಮಾನದಂಡಗಳು ಮತ್ತು ಸಂಬಂಧಿತ ಯೋಜನೆಗಳನ್ನು ತೋರಿಸುತ್ತದೆ.',scheme:'ಯೋಜನೆಗಳನ್ನು ಚಟುವಟಿಕೆಯ ಪ್ರಕಾರ ತೋರಿಸಲಾಗುತ್ತದೆ. ಉದಾಹರಣೆಗೆ ಅರ್ಹ ಕೃಷಿ ಸಾಲಕ್ಕೆ KCC, ಕೃಷಿ ಮೂಲಸೌಕರ್ಯಕ್ಕೆ AIF, ತೋಟಗಾರಿಕೆಗೆ MIDH ಮತ್ತು NHB ಘಟಕಗಳು, ಪಶುಸಂಗೋಪನೆಗೆ NLM, ಮೀನುಗಾರಿಕೆ ಮೂಲಸೌಕರ್ಯಕ್ಕೆ FIDF, ಆಹಾರ ಸಂಸ್ಕರಣೆಗೆ PMFME ಮತ್ತು ಅರ್ಹ ಸೂಕ್ಷ್ಮ ಉದ್ಯಮಗಳಿಗೆ MUDRA ಅಥವಾ PMEGP ಇರಬಹುದು. ಪ್ರಸ್ತುತ ಅಧಿಕೃತ ಮಾರ್ಗಸೂಚಿಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.',market:'ಮಾರುಕಟ್ಟೆ ಬೆಲೆ ಪುಟವು ಲಭ್ಯವಿದ್ದಾಗ ಆಯ್ಕೆ ಮಾಡಿದ ಸ್ಥಳಕ್ಕೆ ಇತ್ತೀಚಿನ ಮಂಡಿ ಮಾಹಿತಿಯನ್ನು ತೋರಿಸಲು ವಿನ್ಯಾಸಗೊಳಿಸಲಾಗಿದೆ. ಮಾರಾಟದ ಮೊದಲು ಮಾರುಕಟ್ಟೆ, ಗುಣಮಟ್ಟ, ಸಾರಿಗೆ ಮತ್ತು ಖರೀದಿದಾರರ ಕಡಿತಗಳನ್ನು ಹೋಲಿಸಿ.',finance:'ಹಣಕಾಸು ಸಹಾಯಕ EMI, ಕೈಗೆಟುಕುವಿಕೆ ಮತ್ತು ನಗದು ಹರಿವು ಮುಂತಾದ ಯೋಜನಾ ಲೆಕ್ಕಾಚಾರಗಳನ್ನು ನೀಡುತ್ತದೆ. ನಿಜವಾದ ಸಾಲದ ನಿಯಮಗಳು ಸಾಲದಾತ ಮತ್ತು ಅನುಮೋದಿತ ಅರ್ಜಿಯ ಮೇಲೆ ಅವಲಂಬಿತವಾಗಿವೆ.',npk:'NPK ಎಂದರೆ ನೈಟ್ರೋಜನ್, ಫಾಸ್ಫರಸ್ ಮತ್ತು ಪೊಟ್ಯಾಸಿಯಂ. ಉಲ್ಲೇಖ ಡೇಟಾ ಲಭ್ಯವಿದ್ದರೆ, ಗ್ರಾಮ ಸಹಾಯಕವು pH, ಆರ್ದ್ರತೆ, ಮಳೆ ಮತ್ತು ತಾಪಮಾನದೊಂದಿಗೆ ಈ ಮೌಲ್ಯಗಳನ್ನು ಬೆಳೆ ಹೊಂದಾಣಿಕೆಯಲ್ಲಿ ಬಳಸಬಹುದು.'}
};

const $ = id => document.getElementById(id);
const q = $('q'), ans = $('answer'), langSel = $('lang'), mic = $('mic'), status = $('status');
let LANG = C.lang;
const L2 = l => (l || '').split('-')[0].toLowerCase();
const ui = () => UI[LANG] || UI['en-IN'];
const current = () => A[LANG] || A['en-IN'];
const setStatus = t => { status.textContent = t || ''; };

/* ---------------- interface text follows the language ---------------- */
function applyUI() {
  const u = ui();
  $('kicker').textContent = u.kicker;
  $('title').textContent = u.title;
  mic.textContent = u.mic;
  $('speak').textContent = u.speak;
  $('stop').textContent = u.stop;
  $('ask').textContent = u.ask;
  q.placeholder = u.placeholder;
  langSel.value = LANG;
  document.documentElement.lang = L2(LANG);
  const box = $('quick'); box.innerHTML = '';
  u.chips.forEach(c => {
    const b = document.createElement('button');
    b.textContent = c[0]; b.dataset.q = c[1];
    b.onclick = () => { q.value = c[1]; askNow(); };
    box.appendChild(b);
  });
}
function showGreeting() {
  const u = ui();
  ans.innerHTML = '';
  const b = document.createElement('b'); b.textContent = u.greetTitle;
  ans.appendChild(b); ans.appendChild(document.createElement('br'));
  ans.appendChild(document.createTextNode(u.greetBody));
}
function show(t) { ans.textContent = t; }

/* ---------------- understanding the question ---------------- */
const INTENTS = [
  ['temp', ['temperature','temp','weather','hot','climate','तापमान','मौसम','गर्मी','ಹವಾಮಾನ','ತಾಪ','ಬಿಸಿ','ಟೆಂಪರೇಚರ್']],
  ['loc', ['location','where','place','स्थान','स्थल','जगह','कहाँ','ಸ್ಥಳ','ಊರು','ಎಲ್ಲಿ']],
  ['business', ['business','recommend','enterprise','व्यवसाय','व्यापार','उद्यम','सिफारिश','सिफ़ारिश','ವ್ಯವಹಾರ','ವ್ಯಾಪಾರ','ಉದ್ಯಮ','ಶಿಫಾರಸ','ಬಿಸಿನೆಸ್']],
  ['scheme', ['scheme','subsid','government','yojana','योजना','योजन','सब्सिडी','सरकारी','ಯೋಜನೆ','ಸಬ್ಸಿಡಿ','ಸರ್ಕಾರಿ','ಸ್ಕೀಮ್']],
  ['market', ['market','mandi','price','rate','bhav','मंडी','बाजार','बाज़ार','भाव','कीमत','ಮಾರುಕಟ್ಟೆ','ಮಂಡಿ','ಬೆಲೆ','ದರ']],
  ['finance', ['loan','emi','finance','financial','money','bank','ऋण','कर्ज','लोन','ईएमआई','वित्त','ಹಣಕಾಸು','ಸಾಲ','ಇಎಂಐ','ಬ್ಯಾಂಕ್']],
  ['npk', ['npk','nitrogen','phosph','potass','नाइट्रोजन','एनपीके','एन पी के','ನೈಟ್ರೋಜನ್','ಎನ್‌ಪಿಕೆ','ಎನ್ ಪಿ ಕೆ']],
  ['how', ['how','work','कैसे','काम','ಹೇಗೆ','ಕೆಲಸ']]
];
function detectIntent(text) {
  const x = (text || '').toLowerCase();
  if (!x.trim()) return 'hello';
  for (const [name, words] of INTENTS) if (words.some(w => x.includes(w))) return name;
  return null;
}
function answerFor(text) {
  const a = current(), it = detectIntent(text);
  if (it === 'hello') return a.hello;
  if (!it) return C.context.page === 'Business Recommendation' ? a.business : (a.hello + ' ' + a.how);
  const v = a[it];
  return typeof v === 'function' ? v() : v;
}

/* ---------------- speaking ---------------- */
// Spoken forms of acronyms so that Kannada / Hindi voices read them naturally.
const SAY = {
  'kn-IN': {KCC:'ಕೆ ಸಿ ಸಿ',AIF:'ಎ ಐ ಎಫ್',MIDH:'ಎಂ ಐ ಡಿ ಎಚ್',NHB:'ಎನ್ ಎಚ್ ಬಿ',NLM:'ಎನ್ ಎಲ್ ಎಂ',FIDF:'ಎಫ್ ಐ ಡಿ ಎಫ್',PMFME:'ಪಿ ಎಂ ಎಫ್ ಎಂ ಇ',MUDRA:'ಮುದ್ರಾ',PMEGP:'ಪಿ ಎಂ ಇ ಜಿ ಪಿ',NPK:'ಎನ್ ಪಿ ಕೆ',EMI:'ಇ ಎಂ ಐ',pH:'ಪಿ ಎಚ್'},
  'hi-IN': {KCC:'के सी सी',AIF:'ए आई एफ',MIDH:'एम आई डी एच',NHB:'एन एच बी',NLM:'एन एल एम',FIDF:'एफ आई डी एफ',PMFME:'पी एम एफ एम ई',MUDRA:'मुद्रा',PMEGP:'पी एम ई जी पी',NPK:'एन पी के',EMI:'ई एम आई',pH:'पी एच'},
  'en-IN': {KCC:'K C C',AIF:'A I F',MIDH:'M I D H',NHB:'N H B',NLM:'N L M',FIDF:'F I D F',PMFME:'P M F M E',PMEGP:'P M E G P',NPK:'N P K',EMI:'E M I'}
};
function speakable(t, lang) {
  let s = String(t || '').replace(/<br\s*\/?>/gi, '. ').replace(/[*_`#]/g, '').replace(/\s+/g, ' ').trim();
  const m = SAY[lang] || {};
  Object.keys(m).forEach(k => { s = s.replace(new RegExp('(^|[^A-Za-z])' + k + '(?![A-Za-z])', 'g'), '$1' + m[k]); });
  return s;
}
function chunkText(t, max) {
  max = max || 170;
  const sentences = (t.match(/[^.!?।॥]+[.!?।॥]*/g) || [t]).map(s => s.trim()).filter(Boolean);
  const out = [];
  sentences.forEach(s => {
    while (s.length > max) {
      let cut = Math.max(s.lastIndexOf(',', max), s.lastIndexOf(' ', max));
      if (cut < max * 0.4) cut = max;
      out.push(s.slice(0, cut).trim());
      s = s.slice(cut).replace(/^[,\s]+/, '');
    }
    if (s) out.push(s);
  });
  // merge tiny neighbours so we make fewer requests
  const merged = [];
  out.forEach(p => {
    if (merged.length && (merged[merged.length - 1] + ' ' + p).length <= max) merged[merged.length - 1] += ' ' + p;
    else merged.push(p);
  });
  return merged;
}

let token = 0, currentAudio = null, voicesCache = [];
function loadVoices(timeout) {
  return new Promise(resolve => {
    if (!('speechSynthesis' in window)) return resolve([]);
    const got = speechSynthesis.getVoices();
    if (got && got.length) { voicesCache = got; return resolve(got); }
    let done = false;
    const finish = () => { if (done) return; done = true; voicesCache = speechSynthesis.getVoices() || []; resolve(voicesCache); };
    try { speechSynthesis.addEventListener('voiceschanged', finish, { once: true }); } catch (e) { speechSynthesis.onvoiceschanged = finish; }
    setTimeout(finish, timeout || 1200);
  });
}
function pickVoice(voices, lang) {
  const want = lang.toLowerCase().replace('_', '-'), base = L2(lang);
  const norm = v => (v.lang || '').toLowerCase().replace('_', '-');
  const score = v => {
    let s = 0; const n = norm(v), nm = (v.name || '').toLowerCase();
    if (n === want) s += 10; else if (n.split('-')[0] === base) s += 6; else return -1;
    if (/natural|online|neural/.test(nm)) s += 3;
    if (/google/.test(nm)) s += 2;
    if (v.localService) s += 1;
    return s;
  };
  let best = null, bs = -1;
  voices.forEach(v => { const s = score(v); if (s > bs) { bs = s; best = v; } });
  if (!best && base === 'kn') best = voices.find(v => /kannada/i.test(v.name || '')) || null;
  if (!best && base === 'hi') best = voices.find(v => /hindi/i.test(v.name || '')) || null;
  return best;
}
function stopSpeaking() {
  token++;
  try { if ('speechSynthesis' in window) speechSynthesis.cancel(); } catch (e) {}
  if (currentAudio) { try { currentAudio.pause(); currentAudio.src = ''; } catch (e) {} currentAudio = null; }
}
function speakWithDevice(chunks, voice, lang, my, done) {
  let i = 0;
  const next = () => {
    if (my !== token) return;
    if (i >= chunks.length) return done(true);
    const u = new SpeechSynthesisUtterance(chunks[i++]);
    u.voice = voice; u.lang = voice.lang || lang; u.rate = 0.95; u.pitch = 1;
    let fired = false;
    u.onend = () => { if (!fired) { fired = true; next(); } };
    u.onerror = e => { if (fired) return; fired = true; if (i === 1 && e && e.error !== 'interrupted' && e.error !== 'canceled') done(false); else next(); };
    speechSynthesis.speak(u);
  };
  next();
}
const TTS_HOSTS = [
  (code, t) => 'https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=' + code + '&q=' + t,
  (code, t) => 'https://translate.googleapis.com/translate_tts?ie=UTF-8&client=gtx&tl=' + code + '&q=' + t
];
function speakWithCloud(chunks, lang, my, done) {
  const code = L2(lang);
  let i = 0;
  const next = () => {
    if (my !== token) return;
    if (i >= chunks.length) return done(true);
    const text = encodeURIComponent(chunks[i]);
    const tryHost = h => {
      if (my !== token) return;
      if (h >= TTS_HOSTS.length) return done(false);
      const a = new Audio(); currentAudio = a;
      let handled = false;
      const fail = () => { if (handled) return; handled = true; tryHost(h + 1); };
      a.onended = () => { if (handled) return; handled = true; i++; next(); };
      a.onerror = fail;
      a.src = TTS_HOSTS[h](code, text);
      const p = a.play();
      if (p && p.catch) p.catch(fail);
    };
    tryHost(0);
  };
  next();
}
async function speakText(raw) {
  const u = ui(), lang = LANG;
  stopSpeaking();
  const my = token;
  const text = speakable(raw, lang);
  if (!text) return;
  const chunks = chunkText(text);
  setStatus(u.speaking);
  const voices = await loadVoices();
  if (my !== token) return;
  const voice = voices.length ? pickVoice(voices, lang) : null;
  const cloud = () => {
    setStatus(u.cloud);
    speakWithCloud(chunks, lang, my, ok => { if (my !== token) return; setStatus(ok ? '' : u.fail); });
  };
  if (voice) {
    setTimeout(() => { if (my !== token) return; setStatus(u.speaking + ' (' + voice.name + ')');
      speakWithDevice(chunks, voice, lang, my, ok => { if (my !== token) return; if (ok) setStatus(''); else cloud(); }); }, 60);
  } else {
    cloud();
  }
}
function askNow() { const t = answerFor(q.value); show(t); speakText(t); }

/* ---------------- wiring ---------------- */
$('ask').onclick = askNow;
$('speak').onclick = () => speakText(ans.innerText);
$('stop').onclick = () => { stopSpeaking(); setStatus(''); };
q.addEventListener('keydown', e => { if (e.key === 'Enter') askNow(); });
langSel.onchange = () => {
  stopSpeaking(); LANG = langSel.value; applyUI(); showGreeting();
  setStatus(ui().langSet + ' ' + langSel.options[langSel.selectedIndex].text);
  if (recog) recog.lang = LANG;
};

const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
let recog = null;
if (!SR) {
  mic.disabled = true; mic.textContent = ui().micNo; setStatus(ui().noSR);
} else {
  recog = new SR();
  recog.continuous = false; recog.interimResults = false; recog.maxAlternatives = 1; recog.lang = LANG;
  recog.onstart = () => { mic.classList.add('listening'); mic.textContent = ui().listening; setStatus(ui().listening); };
  recog.onend = () => { mic.classList.remove('listening'); mic.textContent = ui().mic; };
  recog.onerror = e => {
    mic.classList.remove('listening'); mic.textContent = ui().mic;
    const er = e && e.error;
    setStatus(er === 'not-allowed' || er === 'service-not-allowed' ? ui().micDenied
      : er === 'no-speech' ? ui().noSpeech
      : er === 'language-not-supported' ? ui().srLang : ui().micErr + ' ' + (er || ''));
  };
  recog.onresult = e => {
    const t = e.results[0][0].transcript; q.value = t; setStatus(ui().heard + ' ' + t); askNow();
  };
  mic.onclick = () => { stopSpeaking(); try { recog.lang = LANG; recog.start(); } catch (e) {} };
}
loadVoices();
applyUI(); showGreeting(); setStatus(ui().status);
</script></body></html>
'''

_GS_VOICE_UI = {
    "en-IN": {
        "kicker": "Gram Sahayak Intelligence", "title": "Gram Vaani · AI Voice Assistant",
        "mic": "🎤 Tap & Speak", "listening": "🎙️ Listening… speak now", "speak": "🔊 Read Answer", "stop": "⏹ Stop", "ask": "Ask",
        "placeholder": "Ask about crops, temperature, schemes, loans, markets or business…",
        "greetTitle": "Namaste! / ನಮಸ್ಕಾರ! / Hello!",
        "greetBody": "I am Gram Vaani. Ask me about farming, markets, schemes, finance, crops, business planning, or your selected location.",
        "status": "Voice recognition uses your browser's speech service when supported. Microphone permission is required for Tap & Speak.",
        "langSet": "Language set to", "speaking": "🔊 Speaking…", "cloud": "🔊 Speaking with the online voice…",
        "fail": "Could not play voice on this device. The answer is shown as text above.",
        "micNo": "🎤 Voice unavailable", "noSR": "Voice recognition is not available in this browser. Text and read-aloud still work.",
        "micDenied": "Microphone permission was denied. Please allow it in the browser.", "noSpeech": "No speech was heard. Please try again.",
        "srLang": "This browser cannot recognise this language. Type your question instead.", "micErr": "Microphone error:", "heard": "Heard:",
        "chips": [["How it works", "How does Gram Sahayak work?"], ["🌡️ Temperature", "What is the temperature at my location?"],
                  ["💡 Business", "Tell me about business recommendation"], ["🏛️ Schemes", "Tell me about government schemes"],
                  ["📈 Markets", "Tell me about market prices"], ["🌱 NPK", "Explain NPK"]],
    },
    "hi-IN": {
        "kicker": "ग्राम सहायक इंटेलिजेंस", "title": "ग्राम वाणी · AI आवाज़ सहायक",
        "mic": "🎤 दबाएँ और बोलें", "listening": "🎙️ सुन रहा है… अब बोलें", "speak": "🔊 उत्तर सुनें", "stop": "⏹ रोकें", "ask": "पूछें",
        "placeholder": "फसल, तापमान, योजनाओं, ऋण, बाज़ार या व्यवसाय के बारे में पूछें…",
        "greetTitle": "नमस्ते! / ನಮಸ್ಕಾರ! / Hello!",
        "greetBody": "मैं ग्राम वाणी हूँ। खेती, बाज़ार, योजनाओं, वित्त, फसलों, व्यवसाय योजना या अपने चुने हुए स्थान के बारे में मुझसे पूछें।",
        "status": "आवाज़ पहचान समर्थित होने पर आपके ब्राउज़र की स्पीच सेवा का उपयोग करती है। 'दबाएँ और बोलें' के लिए माइक्रोफ़ोन की अनुमति चाहिए।",
        "langSet": "भाषा चुनी गई:", "speaking": "🔊 बोल रहा है…", "cloud": "🔊 ऑनलाइन आवाज़ से बोल रहा है…",
        "fail": "इस डिवाइस पर आवाज़ नहीं चल सकी। उत्तर ऊपर लिखित रूप में दिखाया गया है।",
        "micNo": "🎤 आवाज़ उपलब्ध नहीं", "noSR": "इस ब्राउज़र में आवाज़ पहचान उपलब्ध नहीं है। लिखकर पूछना और उत्तर सुनना काम करता है।",
        "micDenied": "माइक्रोफ़ोन की अनुमति नहीं मिली। कृपया ब्राउज़र में अनुमति दें।", "noSpeech": "कोई आवाज़ नहीं सुनाई दी। कृपया फिर कोशिश करें।",
        "srLang": "यह ब्राउज़र इस भाषा को नहीं पहचान सकता। कृपया प्रश्न लिखें।", "micErr": "माइक्रोफ़ोन त्रुटि:", "heard": "सुना:",
        "chips": [["कैसे काम करता है", "ग्राम सहायक कैसे काम करता है?"], ["🌡️ तापमान", "मेरे स्थान का तापमान क्या है?"],
                  ["💡 व्यवसाय", "व्यवसाय सिफारिश के बारे में बताइए"], ["🏛️ योजनाएँ", "सरकारी योजनाओं के बारे में बताइए"],
                  ["📈 बाज़ार", "मंडी भाव के बारे में बताइए"], ["🌱 NPK", "NPK समझाइए"]],
    },
    "kn-IN": {
        "kicker": "ಗ್ರಾಮ ಸಹಾಯಕ ಇಂಟೆಲಿಜೆನ್ಸ್", "title": "ಗ್ರಾಮ ವಾಣಿ · AI ಧ್ವನಿ ಸಹಾಯಕ",
        "mic": "🎤 ಒತ್ತಿ ಮಾತನಾಡಿ", "listening": "🎙️ ಕೇಳುತ್ತಿದೆ… ಈಗ ಮಾತನಾಡಿ", "speak": "🔊 ಉತ್ತರ ಓದಿ", "stop": "⏹ ನಿಲ್ಲಿಸಿ", "ask": "ಕೇಳಿ",
        "placeholder": "ಬೆಳೆ, ತಾಪಮಾನ, ಯೋಜನೆ, ಸಾಲ, ಮಾರುಕಟ್ಟೆ ಅಥವಾ ವ್ಯವಹಾರದ ಬಗ್ಗೆ ಕೇಳಿ…",
        "greetTitle": "ನಮಸ್ಕಾರ! / नमस्ते! / Hello!",
        "greetBody": "ನಾನು ಗ್ರಾಮ ವಾಣಿ. ಕೃಷಿ, ಮಾರುಕಟ್ಟೆ, ಯೋಜನೆಗಳು, ಹಣಕಾಸು, ಬೆಳೆಗಳು, ವ್ಯವಹಾರ ಯೋಜನೆ ಅಥವಾ ನೀವು ಆಯ್ಕೆ ಮಾಡಿದ ಸ್ಥಳದ ಬಗ್ಗೆ ನನ್ನನ್ನು ಕೇಳಿ.",
        "status": "ಬೆಂಬಲಿತವಾಗಿದ್ದಾಗ ಧ್ವನಿ ಗುರುತಿಸುವಿಕೆ ನಿಮ್ಮ ಬ್ರೌಸರ್‌ನ ಸ್ಪೀಚ್ ಸೇವೆಯನ್ನು ಬಳಸುತ್ತದೆ. 'ಒತ್ತಿ ಮಾತನಾಡಿ'ಗೆ ಮೈಕ್ರೋಫೋನ್ ಅನುಮತಿ ಬೇಕು.",
        "langSet": "ಭಾಷೆ ಆಯ್ಕೆಯಾಗಿದೆ:", "speaking": "🔊 ಮಾತನಾಡುತ್ತಿದೆ…", "cloud": "🔊 ಆನ್‌ಲೈನ್ ಧ್ವನಿಯಲ್ಲಿ ಮಾತನಾಡುತ್ತಿದೆ…",
        "fail": "ಈ ಸಾಧನದಲ್ಲಿ ಧ್ವನಿ ಪ್ಲೇ ಆಗಲಿಲ್ಲ. ಉತ್ತರ ಮೇಲೆ ಪಠ್ಯರೂಪದಲ್ಲಿ ತೋರಿಸಲಾಗಿದೆ.",
        "micNo": "🎤 ಧ್ವನಿ ಲಭ್ಯವಿಲ್ಲ", "noSR": "ಈ ಬ್ರೌಸರ್‌ನಲ್ಲಿ ಧ್ವನಿ ಗುರುತಿಸುವಿಕೆ ಲಭ್ಯವಿಲ್ಲ. ಟೈಪ್ ಮಾಡಿ ಕೇಳುವುದು ಮತ್ತು ಉತ್ತರ ಕೇಳುವುದು ಕೆಲಸ ಮಾಡುತ್ತದೆ.",
        "micDenied": "ಮೈಕ್ರೋಫೋನ್ ಅನುಮತಿ ನಿರಾಕರಿಸಲಾಗಿದೆ. ದಯವಿಟ್ಟು ಬ್ರೌಸರ್‌ನಲ್ಲಿ ಅನುಮತಿಸಿ.", "noSpeech": "ಯಾವುದೇ ಮಾತು ಕೇಳಿಸಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
        "srLang": "ಈ ಬ್ರೌಸರ್ ಈ ಭಾಷೆಯನ್ನು ಗುರುತಿಸಲಾರದು. ದಯವಿಟ್ಟು ಪ್ರಶ್ನೆಯನ್ನು ಟೈಪ್ ಮಾಡಿ.", "micErr": "ಮೈಕ್ರೋಫೋನ್ ದೋಷ:", "heard": "ಕೇಳಿಸಿದ್ದು:",
        "chips": [["ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ", "ಗ್ರಾಮ ಸಹಾಯಕ ಹೇಗೆ ಕೆಲಸ ಮಾಡುತ್ತದೆ?"], ["🌡️ ತಾಪಮಾನ", "ನನ್ನ ಸ್ಥಳದ ತಾಪಮಾನ ಎಷ್ಟು?"],
                  ["💡 ವ್ಯವಹಾರ", "ವ್ಯವಹಾರ ಶಿಫಾರಸಿನ ಬಗ್ಗೆ ಹೇಳಿ"], ["🏛️ ಯೋಜನೆಗಳು", "ಸರ್ಕಾರಿ ಯೋಜನೆಗಳ ಬಗ್ಗೆ ಹೇಳಿ"],
                  ["📈 ಮಾರುಕಟ್ಟೆ", "ಮಾರುಕಟ್ಟೆ ಬೆಲೆಗಳ ಬಗ್ಗೆ ಹೇಳಿ"], ["🌱 NPK", "NPK ವಿವರಿಸಿ"]],
    },
}
_GS_VOICE_CODES = {"English": "en-IN", "Hindi": "hi-IN", "Kannada": "kn-IN"}


def render_gram_vaani_voice_assistant(page_name, location):
    '''Multilingual voice assistant (English / Hindi / Kannada).
    - Follows the language chosen in the top bar (can also be switched inside the widget).
    - Speech: uses a matching device voice when the browser has one; otherwise streams an
      online voice (this is what makes Kannada work in Chrome, which ships no Kannada voice).'''
    temp, temp_source = get_location_temperature(location)
    water = automatic_location_water(location)
    rainfall = LOCATION_CONTEXT.get(location, {}).get("rainfall_mm", "Not available")
    code = _GS_VOICE_CODES.get(_gs_lang(), "en-IN")
    context = {
        "page": str(page_name),
        "location": tr_place(location),
        "temperature": round(float(temp), 1),
        "temperatureSource": tr_text(str(temp_source)),
        "water": tr_text(str(water)),
        "rainfall": tr_text(str(rainfall)),
        "selectedBusiness": str(st.session_state.get("br_business", "")),
    }
    payload = {"context": context, "lang": code}
    html_code = (_GS_VOICE_TEMPLATE
                 .replace("__CONTEXT__", json.dumps(payload, ensure_ascii=False).replace("</", "<\\/"))
                 .replace("__UI__", json.dumps(_GS_VOICE_UI, ensure_ascii=False).replace("</", "<\\/")))
    components.html(html_code, height=410, scrolling=False)

render_gram_vaani_voice_assistant(page, location)

# ============================================================
# HOME
# ============================================================

if page == "Home":

    st.markdown("""
    <style>
    /* ==================== HOME ONLY ==================== */
    [data-testid="stMainBlockContainer"]{
        max-width:1800px!important;
        padding-left:2.5rem!important;
        padding-right:2.5rem!important;
        padding-top:1.2rem!important;
    }
    .gs-home{animation:gsFade .7s ease both;width:100%}

    /* TOP NAVIGATION */
    .gs-topnav{
        position:sticky;top:0;z-index:999;
        display:flex;align-items:center;justify-content:space-between;
        gap:22px;padding:13px 20px;margin:0 0 20px;
        border-radius:18px;background:rgba(255,255,255,.90);
        border:1px solid rgba(55,105,50,.12);
        box-shadow:0 10px 30px rgba(35,75,35,.10);
        backdrop-filter:blur(14px);
    }
    .gs-brand{display:flex;align-items:center;gap:9px;white-space:nowrap;font-size:18px;font-weight:900;color:#315b2c}
    .gs-navlinks{display:flex;align-items:center;justify-content:flex-end;gap:6px;flex-wrap:wrap}
    .gs-navlinks a{
        text-decoration:none!important;color:#40543c!important;font-size:13px;font-weight:750;
        padding:9px 13px;border-radius:999px;transition:all .25s ease;
    }
    .gs-navlinks a:hover{background:#eaf4e6;transform:translateY(-2px);color:#2f6429!important}

    /* HERO */
    .gs-hero{
        position:relative;min-height:620px;overflow:hidden;border-radius:34px;margin-bottom:18px;
        background:#edf6e9;border:1px solid rgba(54,105,52,.12);
        box-shadow:0 24px 65px rgba(35,75,35,.16)
    }
    .gs-hero-copy{position:relative;z-index:5;width:53%;padding:78px 46px 70px 68px;animation:gsSlide .8s ease both}
    .gs-kicker{display:inline-block;padding:9px 16px;border-radius:999px;background:rgba(255,255,255,.78);border:1px solid rgba(55,105,50,.12);font-size:12px;font-weight:800;letter-spacing:1.1px;text-transform:uppercase}
    .gs-hero-title{font-size:68px;line-height:1.0;margin:23px 0 15px;font-weight:900;letter-spacing:-2.8px}
    .gs-hero-subtitle{font-size:31px;line-height:1.22;font-weight:780;margin-bottom:15px;max-width:700px}
    .gs-hero-text{font-size:17px;line-height:1.75;max-width:650px;opacity:.72}
    .gs-hero-stage{margin-top:23px;font-size:13px;font-weight:750;opacity:.62}
    .gs-hero-visual{position:absolute;right:0;top:0;width:57%;height:100%;overflow:hidden}
    .gs-photo{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;animation:gsZoom 7s ease-in-out infinite alternate;filter:saturate(.95)}
    .gs-photo-overlay{position:absolute;inset:0;background:linear-gradient(90deg,#edf6e9 0%,rgba(237,246,233,.91) 10%,rgba(237,246,233,.30) 50%,rgba(237,246,233,0) 100%)}
    .gs-floating-leaf{position:absolute;z-index:4;font-size:34px;animation:gsFloat 4s ease-in-out infinite}
    .gs-leaf1{right:42%;top:15%}.gs-leaf2{right:10%;bottom:18%;animation-delay:1.3s}.gs-leaf3{right:28%;bottom:8%;font-size:24px;animation-delay:.6s}

    .gs-explore-row{text-align:center;margin:0 0 55px}
    .gs-explore-row .stButton>button{
        border-radius:999px!important;padding:13px 31px!important;font-size:15px!important;
        font-weight:850!important;background:#3f7338!important;color:white!important;border:0!important;
        box-shadow:0 12px 27px rgba(48,100,43,.24)!important;transition:all .25s ease!important
    }
    .gs-explore-row .stButton>button:hover{transform:translateY(-4px) scale(1.025)!important;box-shadow:0 17px 34px rgba(48,100,43,.30)!important}
    .gs-progress{height:5px;max-width:360px;margin:13px auto 0;background:rgba(60,110,55,.12);border-radius:20px;overflow:hidden}
    .gs-progress span{display:block;height:100%;background:#4f813f;border-radius:20px;transition:width .5s ease}

    /* SECTIONS */
    .gs-section{scroll-margin-top:95px}
    .gs-heading{text-align:center;font-size:34px;font-weight:850;margin:0}
    .gs-note{text-align:center;opacity:.62;margin:9px 0 28px;font-size:15px}
    .gs-feature-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-bottom:58px}
    .gs-card{min-height:190px;padding:28px 23px;border-radius:23px;background:rgba(255,255,255,.92);border:1px solid rgba(65,105,55,.12);box-shadow:0 11px 30px rgba(40,70,35,.09);transition:transform .3s ease,box-shadow .3s ease;animation:gsCard .65s ease both}
    .gs-card:hover{transform:translateY(-10px) rotate(.25deg);box-shadow:0 20px 40px rgba(40,70,35,.17)}
    .gs-icon{font-size:39px;margin-bottom:13px;animation:gsIcon 2.8s ease-in-out infinite}
    .gs-card-title{font-size:19px;font-weight:800;margin-bottom:8px}.gs-card-text{font-size:14px;line-height:1.65;opacity:.65}

    .gs-glance{padding:40px 32px;border-radius:29px;background:linear-gradient(135deg,#eef7e9,#faf4e0);border:1px solid rgba(65,105,55,.1);margin-bottom:58px;scroll-margin-top:95px}
    .gs-glance-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:17px;margin-top:28px}
    .gs-glance-item{padding:25px 17px;border-radius:19px;background:rgba(255,255,255,.86);text-align:center;border:1px solid rgba(65,105,55,.09);transition:all .25s ease}
    .gs-glance-item:hover{transform:translateY(-6px);box-shadow:0 12px 25px rgba(40,70,35,.09)}
    .gs-glance-icon{font-size:31px}.gs-glance-label{font-size:12px;opacity:.58;margin-top:9px}.gs-glance-value{font-size:16px;font-weight:760;margin-top:6px}

    .gs-how{margin-bottom:58px;scroll-margin-top:95px}.gs-process{display:flex;align-items:center;justify-content:center;gap:12px;margin-top:30px}
    .gs-step{flex:1;max-width:255px;padding:25px 15px;text-align:center;border-radius:21px;background:rgba(255,255,255,.86);border:1px solid rgba(65,105,55,.11);box-shadow:0 8px 24px rgba(40,70,35,.07);animation:gsCard .7s ease both}
    .gs-number{width:47px;height:47px;border-radius:50%;margin:0 auto 12px;display:flex;align-items:center;justify-content:center;background:#477a3c;color:white;font-weight:850;animation:gsPulse 2s infinite}
    .gs-step-title{font-size:15px;font-weight:780}.gs-step-text{font-size:12px;line-height:1.5;opacity:.62;margin-top:6px}.gs-arrow{font-size:29px;opacity:.4;animation:gsArrow 1.4s ease-in-out infinite}

    .gs-motion{display:grid;grid-template-columns:1.05fr 1fr;gap:30px;align-items:center;padding:28px;border-radius:29px;background:#f4f7ef;border:1px solid rgba(65,105,55,.1);margin-bottom:58px}
    .gs-gif{height:320px;border-radius:23px;overflow:hidden;background:#dfe9d8;box-shadow:0 14px 35px rgba(40,70,35,.13)}.gs-gif img{width:100%;height:100%;object-fit:cover}
    .gs-motion h2{font-size:31px;margin:0 0 13px}.gs-motion p{line-height:1.75;opacity:.68}.gs-badges{display:flex;flex-wrap:wrap;gap:9px;margin-top:18px}.gs-badge{padding:8px 13px;border-radius:999px;background:white;border:1px solid rgba(65,105,55,.1);font-size:12px;font-weight:700}

    .gs-built{display:grid;grid-template-columns:1fr 1fr;gap:34px;align-items:center;padding:30px;border-radius:29px;background:rgba(246,248,241,.86);border:1px solid rgba(65,105,55,.1);margin-bottom:58px;scroll-margin-top:95px}
    .gs-built-img{height:390px;border-radius:23px;overflow:hidden}.gs-built-img img{width:100%;height:100%;object-fit:cover;transition:transform .7s ease}.gs-built-img:hover img{transform:scale(1.07)}
    .gs-built h2{font-size:34px;margin:0 0 14px}.gs-built p{line-height:1.75;opacity:.68}.gs-checks{list-style:none;padding:0}.gs-checks li{margin:12px 0;font-weight:650;animation:gsSlide .5s ease both}

    .gs-cta{text-align:center;padding:54px 28px;border-radius:30px;background:linear-gradient(135deg,#edf6e9,#f8f2dd);border:1px solid rgba(65,105,55,.1);margin-bottom:25px;box-shadow:0 14px 38px rgba(40,70,35,.09)}
    .gs-cta h2{font-size:34px;margin:0 0 10px}.gs-cta p{opacity:.65;margin-bottom:21px}

    @keyframes gsFade{from{opacity:0}to{opacity:1}}
    @keyframes gsSlide{from{opacity:0;transform:translateX(-25px)}to{opacity:1;transform:translateX(0)}}
    @keyframes gsCard{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
    @keyframes gsZoom{from{transform:scale(1)}to{transform:scale(1.08)}}
    @keyframes gsFloat{0%,100%{transform:translateY(0) rotate(-5deg)}50%{transform:translateY(-16px) rotate(8deg)}}
    @keyframes gsIcon{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
    @keyframes gsArrow{0%,100%{transform:translateX(0)}50%{transform:translateX(8px)}}
    @keyframes gsPulse{0%,100%{box-shadow:0 0 0 0 rgba(71,122,60,.25)}50%{box-shadow:0 0 0 8px rgba(71,122,60,0)}}

    @media(max-width:1100px){
        [data-testid="stMainBlockContainer"]{padding-left:1.5rem!important;padding-right:1.5rem!important}
        .gs-feature-grid,.gs-glance-grid{grid-template-columns:repeat(2,1fr)}
        .gs-hero-copy{width:62%;padding-left:48px}.gs-hero-visual{width:51%}.gs-hero-title{font-size:56px}
        .gs-navlinks a{padding:8px 9px;font-size:12px}
    }
    @media(max-width:760px){
        [data-testid="stMainBlockContainer"]{padding-left:.7rem!important;padding-right:.7rem!important}
        .gs-topnav{position:relative;display:block;padding:14px;margin-bottom:14px}.gs-brand{justify-content:center;margin-bottom:10px}.gs-navlinks{justify-content:center}
        .gs-hero{min-height:720px}.gs-hero-copy{width:100%;padding:38px 24px}.gs-hero-title{font-size:45px}.gs-hero-subtitle{font-size:23px}.gs-hero-text{font-size:15px}
        .gs-hero-visual{width:100%;height:43%;top:auto;bottom:0}.gs-photo-overlay{background:linear-gradient(180deg,#edf6e9 0%,rgba(237,246,233,.30) 35%,rgba(237,246,233,0) 100%)}
        .gs-feature-grid,.gs-glance-grid,.gs-motion,.gs-built{grid-template-columns:1fr}.gs-process{flex-direction:column}.gs-step{width:100%;max-width:440px}.gs-arrow{transform:rotate(90deg)}
        .gs-gif{height:250px}.gs-built-img{height:290px}.gs-heading{font-size:28px}.gs-built h2,.gs-motion h2,.gs-cta h2{font-size:28px}
    }
    </style>
    """, unsafe_allow_html=True)

    if "gs_scene" not in st.session_state:
        st.session_state.gs_scene = 0

    scenes = [
        {
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1500&q=88",
            "title": "Your Digital Companion for Smarter Farming",
            "text": "Get useful information about crops, market prices, government schemes and financial guidance — all in one place.",
            "stage": "01 / 03"
        },
        {
            "image": "https://images.unsplash.com/photo-1464226184884-fa280b87c399?auto=format&fit=crop&w=1500&q=88",
            "title": "Discover Better Farming Information",
            "text": "Explore crop information and practical agricultural guidance through a simple farmer-friendly interface.",
            "stage": "02 / 03"
        },
        {
            "image": "https://images.unsplash.com/photo-1488459716781-31db52582fe9?auto=format&fit=crop&w=1500&q=88",
            "title": "Make Informed Decisions",
            "text": "Check available mandi prices, explore schemes and use financial guidance to support your next step.",
            "stage": "03 / 03"
        }
    ]
    scene = scenes[st.session_state.gs_scene]

    st.markdown(f"""
    <div class="gs-home">
      <div class="gs-hero">
        <div class="gs-hero-copy">
          <div class="gs-kicker">🌱 Agriculture • Information • Guidance</div>
          <h1 class="gs-hero-title">🌾 Gram Sahayak</h1>
          <div class="gs-hero-subtitle">{scene['title']}</div>
          <p class="gs-hero-text">{scene['text']}</p>
        </div>
        <div class="gs-hero-visual">
          <img class="gs-photo" src="{scene['image']}" alt="Agriculture and farming">
          <div class="gs-photo-overlay"></div>
          <div class="gs-floating-leaf gs-leaf1">🌿</div>
          <div class="gs-floating-leaf gs-leaf2">🍃</div>
          <div class="gs-floating-leaf gs-leaf3">🌱</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div id="gs-features" class="gs-section">
      <h2 class="gs-heading">✨ Explore Gram Sahayak</h2>
      <p class="gs-note">Useful tools gathered in one simple farmer-friendly interface.</p>
      <div class="gs-feature-grid">
        <div class="gs-card"><div class="gs-icon">🌾</div><div class="gs-card-title">Crop Information</div><div class="gs-card-text">Learn about crops and farming practices.</div></div>
        <div class="gs-card"><div class="gs-icon">💰</div><div class="gs-card-title">Market Prices</div><div class="gs-card-text">Check the latest available mandi prices.</div></div>
        <div class="gs-card"><div class="gs-icon">🏛️</div><div class="gs-card-title">Government Schemes</div><div class="gs-card-text">Explore useful government agricultural schemes.</div></div>
        <div class="gs-card"><div class="gs-icon">🤖</div><div class="gs-card-title">Financial Assistant</div><div class="gs-card-text">Get simple financial guidance for farming.</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div id="gs-glance" class="gs-glance gs-section">
      <h2 class="gs-heading">🌱 Farming at a Glance</h2>
      <p class="gs-note">A quick overview using information already available in the app.</p>
      <div class="gs-glance-grid">
        <div class="gs-glance-item"><div class="gs-glance-icon">📍</div><div class="gs-glance-label">Location</div><div class="gs-glance-value">{str(location)}</div></div>
        <div class="gs-glance-item"><div class="gs-glance-icon">🌾</div><div class="gs-glance-label">Crop</div><div class="gs-glance-value">Select in Crop Information</div></div>
        <div class="gs-glance-item"><div class="gs-glance-icon">💰</div><div class="gs-glance-label">Market Price</div><div class="gs-glance-value">Latest available in Market Prices</div></div>
        <div class="gs-glance-item"><div class="gs-glance-icon">🏛️</div><div class="gs-glance-label">Government Schemes</div><div class="gs-glance-value">Available in the Government Schemes page</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div id="gs-how" class="gs-how gs-section">
      <h2 class="gs-heading">⚙️ How Gram Sahayak Works</h2>
      <p class="gs-note">A location-aware digital farm companion: understand → compare → plan → act, with Gram Vaani available for voice guidance in English, Hindi and Kannada.</p>
      <div class="gs-process">
        <div class="gs-step"><div class="gs-number">1</div><div class="gs-step-title">📍 Set Your Location</div><div class="gs-step-text">Choose your location once. Gram Sahayak reuses it for climate context, temperature, water profile, market context and business planning.</div></div>
        <div class="gs-arrow">→</div>
        <div class="gs-step"><div class="gs-number">2</div><div class="gs-step-title">🌾 Explore the Right Tool</div><div class="gs-step-text">Move between Crop Information, Market Prices, Government Schemes, Financial Assistant and Business Recommendation without repeatedly entering your location.</div></div>
        <div class="gs-arrow">→</div>
        <div class="gs-step"><div class="gs-number">3</div><div class="gs-step-title">🧠 Personalise the Assessment</div><div class="gs-step-text">Enter only the relevant details. Business Recommendation adds species/variety/product selection and automatically brings location-based temperature into the assessment.</div></div>
        <div class="gs-arrow">→</div>
        <div class="gs-step"><div class="gs-number">4</div><div class="gs-step-title">📊 Turn Information into Action</div><div class="gs-step-text">Receive practical outputs: crop/environment matching, mandi information, scheme discovery, financial planning and business roadmaps with risks and next steps.</div></div>
        <div class="gs-arrow">→</div>
        <div class="gs-step"><div class="gs-number">5</div><div class="gs-step-title">🎙️ Ask Gram Vaani</div><div class="gs-step-text">Use the multilingual voice assistant to ask about your location, temperature, crops, markets, schemes, finance or business planning in English, Hindi or Kannada.</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="gs-motion" id="gs-smart-farming">
      <div class="gs-gif"><img src="https://media.giphy.com/media/mDBBU8K7Np2UQs9Dqy/giphy.gif" alt="Seedlings growing animation"></div>
      <div>
        <div class="gs-kicker">🌱 From Seed to Harvest</div>
        <h2>Grow Smarter with Gram Sahayak</h2>
        <p>Get crop information, market updates, scheme details and financial guidance to support better farming decisions.</p>
        <div class="gs-badges"><span class="gs-badge">🌱 Crop Information</span><span class="gs-badge">📈 Market Updates</span><span class="gs-badge">🏛️ Schemes</span><span class="gs-badge">💰 Financial Guidance</span></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div id="gs-built" class="gs-built gs-section">
      <div class="gs-built-img"><img src="https://images.unsplash.com/photo-1464226184884-fa280b87c399?auto=format&fit=crop&w=1200&q=88" alt="Farmer and agricultural produce"></div>
      <div>
        <h2>👨‍🌾 Built for Farmers</h2>
        <p>Gram Sahayak brings important agricultural information together in a simple and accessible interface.</p>
        <ul class="gs-checks"><li>✓ Simple to use</li><li>✓ Agricultural information</li><li>✓ Latest available mandi prices</li><li>✓ Government scheme information</li><li>✓ Financial guidance</li></ul>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="gs-cta">
      <h2>🌱 Everything you need, in one place.</h2>
      <p>Explore Gram Sahayak and discover useful tools for smarter farming.</p>
    </div>
    """, unsafe_allow_html=True)



# ============================================================
# LIVE MANDI / AGMARKNET CONNECTION — ADDITION ONLY
# ============================================================
# The complete original Market Prices implementation below is preserved.
# This new interface is rendered first and stops before the legacy block.
MANDI_RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070"
MANDI_API_URL = f"https://api.data.gov.in/resource/{MANDI_RESOURCE_ID}"
MANDI_STATE = "India"  # legacy compatibility constant; selected state/UT is used at runtime

# ------------------------------------------------------------
# data.gov.in API KEY
# ------------------------------------------------------------
# The key is entered by the user on the Market Prices page (as before).
# A default can optionally be pre-filled from .streamlit/secrets.toml.
DEFAULT_MANDI_API_KEY = ""
try:
    DEFAULT_MANDI_API_KEY = st.secrets.get("MANDI_API_KEY", "") or ""
except Exception:
    DEFAULT_MANDI_API_KEY = ""


def _mandi_norm(value):
    return " ".join(str(value or "").strip().lower().split())


def _mandi_num(value):
    try:
        return float(str(value).replace(",", "").strip())
    except Exception:
        return None


# ------------------------------------------------------------
# LOCATION -> MANDI DISTRICT
# ------------------------------------------------------------
# The location chosen in the top navigation bar is used everywhere in the
# app. Many of those locations are taluks/towns, while the government mandi
# dataset is published district-wise, so each location is mapped to the
# district under which its mandi records are reported.
# Crop name (app) -> commodity names used in the government mandi dataset.
MANDI_COMMODITY_ALIASES = {
    "Green Chilli": ["Green Chilli", "Green Chilli (Fresh)", "Chilli Green", "Chilli", "Green Chilli Fresh"],
    "Chilli": ["Chilli", "Green Chilli", "Chillies", "Red Chilli", "Dry Chillies", "Chilly Capsicum"],
    "Lady Finger": ["Lady Finger", "Bhindi", "Okra", "Bhindi(Ladies Finger)"],
    "Brinjal": ["Brinjal", "Eggplant", "Brinjal (Purple)"],
    "Coriander": ["Coriander", "Coriander Seed", "Dhaniya", "Coriander(Leaves)"],
    "Groundnut": ["Groundnut", "Ground Nut", "Peanut", "Groundnut (Split)", "Groundnut Seed"],
    "Areca nut": ["Arecanut", "Areca nut", "Areca Nut", "Supari", "Arecanut(Betelnut/Supari)"],
    "Bengal Gram": ["Bengal Gram", "Bengal Gram(Gram)(Whole)", "Gram", "Chana", "Kabuli Chana"],
    "Black Gram": ["Black Gram", "Black Gram (Urd Beans)(Whole)", "Black Gram Dal", "Urad", "Urad Dal"],
    "Green Gram": ["Green Gram", "Green Gram (Moong)(Whole)", "Green Gram Dal", "Moong", "Moong Dal"],
    "Tur": ["Tur", "Arhar", "Arhar (Tur/Red Gram)(Whole)", "Arhar Dal", "Red Gram", "Tur Dal"],
    "Jowar": ["Jowar", "Jowar(Sorghum)", "Sorghum"],
    "Bajra": ["Bajra", "Bajra(Pearl Millet/Cumbu)", "Pearl Millet"],
    "Maize": ["Maize", "Corn"],
    "Paddy": ["Paddy", "Paddy(Dhan)(Common)", "Paddy(Dhan)(Basmati)", "Rice"],
    "Cotton": ["Cotton", "Cotton (Unginned)", "Kapas"],
    "Sugarcane": ["Sugarcane"],
    "Sunflower": ["Sunflower", "Sunflower Seed"],
    "Soybean": ["Soyabean", "Soybean", "Soyabean Yellow"],
    "Tomato": ["Tomato"],
    "Onion": ["Onion", "Onions"],
    "Potato": ["Potato"],
    "Mango": ["Mango", "Mango (Raw-Ripe)"],
    "Grapes": ["Grapes"],
    "Pomegranate": ["Pomegranate", "Pomegranate (Anar)"],
    "Turmeric": ["Turmeric", "Turmeric Raw", "Turmeric (raw)"],
    "Coffee": ["Coffee", "Coffee Beans"],
    "Pepper": ["Black Pepper", "Pepper", "Pepper ungarbled", "Pepper garbled"],
    "Cardamom": ["Cardamom", "Cardamoms"],
    "Coconut": ["Coconut", "Coconut Seed", "Coconut Oil", "Tender Coconut"],
    "Cashew": ["Cashew", "Cashewnuts", "Cashew Nut", "Cashewnut"],
    "Banana": ["Banana", "Banana - Green"],
    "Orange": ["Orange", "Orange (Nagpur)"],
    "Ragi": ["Ragi", "Ragi (Finger Millet)", "Finger Millet"],
    "Wheat": ["Wheat"],
    "Tobacco": ["Tobacco"],
    "Rubber": ["Rubber"],
    "Mulberry": ["Mulberry", "Mulberry Leaf", "Cocoon", "Mulberry Cocoon"],
    "Flowers": ["Rose(Loose)", "Marigold(Calcutta)", "Jasmine", "Chrysanthemum(Loose)", "Marigold(Loose)"],
    "Vegetables": ["Tomato", "Onion", "Potato", "Brinjal", "Cabbage", "Cauliflower", "Beans"],
    "Spices": ["Pepper", "Cardamom", "Turmeric", "Chilli", "Coriander"],
}

# Some AGRI_LOCATION_CROPS entries list a broad category rather than a single
# crop. This map expands each category into the individual crops that should
# get their own price card, styled the same way as every other crop.
CATEGORY_EXPANSION = {
    "Vegetables": ["Tomato", "Onion", "Potato", "Brinjal", "Cabbage", "Cauliflower", "Beans"],
    "Spices": ["Pepper", "Cardamom", "Turmeric", "Coriander"],
}

# Reverse map: normalised commodity text -> app crop name.
_MANDI_COMMODITY_LOOKUP = {}
for _crop, _names in MANDI_COMMODITY_ALIASES.items():
    for _name in _names:
        _MANDI_COMMODITY_LOOKUP.setdefault(_mandi_norm(_name), []).append(_crop)


def _mandi_date_key(row):
    raw = str(row.get("arrival_date", "")).strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.datetime.strptime(raw, fmt)
        except Exception:
            pass
    return datetime.datetime.min


def _mandi_request(params):
    """Single request with one retry on timeout/connection problems."""
    last_error = None
    for attempt in range(2):
        try:
            response = requests.get(
                MANDI_API_URL,
                params=params,
                timeout=(8, 20),
                headers={"User-Agent": "Gram-Sahayak/1.0"},
            )
            response.raise_for_status()
            payload = response.json()
            records = payload.get("records", []) if isinstance(payload, dict) else []
            return records, None
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as exc:
            last_error = "The government mandi server took too long to respond. Please try again in a moment."
            if attempt == 0:
                import time
                time.sleep(1.0)
        except Exception as exc:
            message = str(exc)
            # Never show the API key back to the user in an error message.
            message = message.split("?")[0]
            if "401" in message or "403" in message:
                message = ("The data.gov.in service rejected this API key. "
                           "Please check the key entered above, or generate a free "
                           "key at data.gov.in.")
            return [], message
    return [], last_error


@st.cache_data(ttl=900, show_spinner=False)
def _fetch_state_records(state, api_key):
    """Fetch live mandi records for the selected state/UT."""
    if not api_key:
        return [], "Enter your data.gov.in API key above to load live mandi prices."
    if requests is None:
        return [], "The requests package is not installed. Run: pip install requests"
    got, err = _mandi_request({
        "api-key": api_key, "format": "json", "limit": 2000, "offset": 0,
        "filters[state]": state,
    })
    return got, err


def _best_record(records, crop, taluka=None):
    """
    Latest usable price record for one crop from a list of mandi records.

    When a taluka is given, only mandis whose market name matches that taluka
    are considered, so the cards can show the taluka's own mandi first.
    """
    wanted = {_mandi_norm(n) for n in MANDI_COMMODITY_ALIASES.get(crop, [crop])}
    taluka_key = _mandi_norm(taluka) if taluka else None
    matches = []
    for row in records:
        commodity = _mandi_norm(row.get("commodity"))
        if not commodity:
            continue
        if taluka_key:
            market = _mandi_norm(row.get("market"))
            if taluka_key not in market and market not in taluka_key:
                continue
        if commodity in wanted or any(w and (w in commodity or commodity in w) for w in wanted):
            matches.append(row)
    if not matches:
        return None

    matches.sort(key=_mandi_date_key, reverse=True)
    for row in matches:
        mn = _mandi_num(row.get("min_price"))
        md = _mandi_num(row.get("modal_price"))
        mx = _mandi_num(row.get("max_price"))
        if mn is None and md is None and mx is None:
            continue
        values = [v for v in (mn, md, mx) if v is not None]
        return {
            "commodity": row.get("commodity", crop),
            "market": row.get("market", "Not reported"),
            "district": row.get("district", "Not reported"),
            "date": row.get("arrival_date", "Not reported"),
            "min": mn if mn is not None else min(values),
            "modal": md if md is not None else max(values),
            "max": mx if mx is not None else max(values),
            "variety": row.get("variety", ""),
        }
    return None


# Master crop list: every crop that appears anywhere in AGRI_LOCATION_CROPS,
# with the broad "Vegetables"/"Spices" categories expanded into their
# individual crops. This is the same list of price cards shown for every
# location, so no location shows a shorter list than another.
_ALL_LOCATION_CROPS = set()
for _crop_list in AGRI_LOCATION_CROPS.values():
    _ALL_LOCATION_CROPS.update(_crop_list)

ALL_MARKET_CROPS = []
_seen_market_crops = set()
for _crop in sorted(_ALL_LOCATION_CROPS):
    for _expanded in CATEGORY_EXPANSION.get(_crop, [_crop]):
        if _expanded not in _seen_market_crops:
            _seen_market_crops.add(_expanded)
            ALL_MARKET_CROPS.append(_expanded)
ALL_MARKET_CROPS.sort()


def get_mandi_prices(state, api_key):
    """Latest mandi price for every configured crop in the selected state/UT."""
    state_records, error = _fetch_state_records(state, api_key)
    results = []
    for crop in ALL_MARKET_CROPS:
        record = _best_record(state_records, crop)
        if record: record["scope"] = "state"
        results.append((crop, record))
    return results, error



# ============================================================
# CROP CARD IMAGES
# ============================================================
@st.cache_data(ttl=86400, show_spinner=False)
@st.cache_data(ttl=86400, show_spinner=False)
def get_crop_image_urls(crops):
    """Return an image for every crop/fruit/vegetable card.

    The old implementation depended on an exact English Wikipedia article
    title, so crops such as Bajra, Jowar, Ragi, Tur and local names could lose
    their picture.  This version tries several well-known aliases in one
    Wikipedia request and matches the first available thumbnail back to the
    original crop name.  A failure for one crop never prevents the market page
    from rendering.
    """
    crops = [str(c).strip() for c in crops if str(c).strip()]
    if requests is None or not crops:
        return {c: None for c in crops}

    aliases = {
        "Areca nut": ["Areca nut", "Areca catechu"],
        "Bajra": ["Bajra", "Pearl millet", "Pearl millet grain"],
        "Jowar": ["Jowar", "Sorghum", "Sorghum bicolor"],
        "Ragi": ["Ragi", "Finger millet", "Eleusine coracana"],
        "Tur": ["Tur", "Pigeon pea", "Cajanus cajan"],
        "Groundnut": ["Groundnut", "Peanut", "Arachis hypogaea"],
        "Beans": ["Green bean", "Common bean", "Beans"],
        "Brinjal": ["Brinjal", "Eggplant", "Aubergine"],
        "Chilli": ["Chilli pepper", "Chili pepper", "Capsicum annuum"],
        "Coriander": ["Coriander", "Coriander seed", "Cilantro"],
        "Cardamom": ["Cardamom", "Elettaria cardamomum"],
        "Turmeric": ["Turmeric", "Curcuma longa"],
        "Paddy": ["Rice", "Paddy field", "Oryza sativa"],
        "Maize": ["Maize", "Corn", "Zea mays"],
        "Cotton": ["Cotton", "Gossypium"],
        "Sugarcane": ["Sugarcane", "Saccharum officinarum"],
        "Soybean": ["Soybean", "Glycine max"],
        "Mulberry": ["Mulberry", "Morus alba"],
        "Arecanut": ["Areca nut", "Areca catechu"],
        "Coconut": ["Coconut", "Cocos nucifera"],
        "Cashew": ["Cashew", "Cashew nut", "Anacardium occidentale"],
        "Pepper": ["Black pepper", "Piper nigrum"],
        "Potato": ["Potato", "Solanum tuberosum"],
        "Tomato": ["Tomato", "Solanum lycopersicum"],
        "Onion": ["Onion", "Allium cepa"],
        "Cabbage": ["Cabbage", "Brassica oleracea"],
        "Cauliflower": ["Cauliflower", "Brassica oleracea botrytis"],
        "Banana": ["Banana", "Musa"],
        "Mango": ["Mango", "Mangifera indica"],
        "Grapes": ["Grape", "Grapes", "Vitis vinifera"],
        "Pomegranate": ["Pomegranate", "Punica granatum"],
        "Papaya": ["Papaya", "Carica papaya"],
        "Watermelon": ["Watermelon", "Citrullus lanatus"],
        "Pineapple": ["Pineapple", "Ananas comosus"],
    }

    titles=[]
    crop_title_candidates={}
    for crop in crops:
        candidates=aliases.get(crop, [crop])
        crop_title_candidates[crop]=candidates
        titles.extend(candidates)
    # Remove duplicate titles while preserving order.
    titles=list(dict.fromkeys(titles))

    found={}
    try:
        for offset in range(0, len(titles), 40):
            batch=titles[offset:offset+40]
            params={
                "action":"query", "format":"json", "prop":"pageimages",
                "piprop":"thumbnail", "pithumbsize":640, "redirects":1,
                "titles":"|".join(batch),
            }
            r=requests.get("https://en.wikipedia.org/w/api.php", params=params,
                           headers={"User-Agent":"GramSahayak/1.0"}, timeout=10)
            r.raise_for_status()
            pages=r.json().get("query",{}).get("pages",{})
            for page in pages.values():
                title=str(page.get("title",""))
                source=page.get("thumbnail",{}).get("source")
                if source:
                    found[title.casefold()]=source
    except Exception:
        # Return any images already found; cards without images still render.
        pass

    result={}
    for crop in crops:
        url=None
        for candidate in crop_title_candidates[crop]:
            url=found.get(candidate.casefold())
            if url:
                break
        # Second-pass fuzzy title match catches redirects such as
        # "Grape" -> "Grape" and scientific-name pages.
        if not url:
            for candidate in crop_title_candidates[crop]:
                c=candidate.casefold()
                for title, image_url in found.items():
                    if c in title or title in c:
                        url=image_url
                        break
                if url:
                    break
        result[crop]=url

    # Commons fallback: some local/common crop names have no useful English
    # Wikipedia article thumbnail. Search Wikimedia Commons for a real image
    # only for those missing crops. This makes the picture layer much more
    # complete without changing the mandi data itself.
    missing=[c for c in crops if not result.get(c)]
    if missing and requests is not None:
        try:
            from concurrent.futures import ThreadPoolExecutor, as_completed
            def _commons_image(crop):
                query=crop_title_candidates.get(crop, [crop])[0]
                params={
                    "action":"query", "format":"json", "generator":"search",
                    "gsrsearch":f"{query} filetype:bitmap", "gsrnamespace":6,
                    "gsrlimit":3, "prop":"imageinfo", "iiprop":"url",
                    "iiurlwidth":640,
                }
                try:
                    rr=requests.get("https://commons.wikimedia.org/w/api.php",
                                     params=params, headers={"User-Agent":"GramSahayak/1.0"}, timeout=7)
                    rr.raise_for_status()
                    pages=rr.json().get("query",{}).get("pages",{})
                    for page in pages.values():
                        info=(page.get("imageinfo") or [{}])[0]
                        u=info.get("thumburl") or info.get("url")
                        if u:
                            return crop,u
                except Exception:
                    pass
                return crop,None
            with ThreadPoolExecutor(max_workers=min(8,len(missing))) as ex:
                futures=[ex.submit(_commons_image,c) for c in missing]
                for fut in as_completed(futures):
                    crop,url=fut.result()
                    if url:
                        result[crop]=url
        except Exception:
            pass

    return result

# ============================================================
# MARKET PRICES — LIVE KARNATAKA MANDI PRICES
# ============================================================
if page == "Market Prices":
    st.markdown("""
    <style>
    .gs-price-grid-note{color:#6B7280;font-size:13.5px;margin:.2rem 0 1rem;}
    .gs-price-card{
        background:#FFFFFF;border:1px solid rgba(46,125,50,.18);border-radius:14px;
        padding:16px 18px;margin-bottom:14px;min-height:172px;
        box-shadow:0 4px 6px -1px rgba(0,0,0,.08),0 10px 20px rgba(27,94,32,.05);
    }
    .gs-price-card.empty{background:#FAFAFA;border-style:dashed;}
    .gs-price-crop{font-size:17px;font-weight:800;color:#1B5E20;margin-bottom:6px;}
    .gs-price-modal{font-size:28px;font-weight:900;color:#2E7D32;line-height:1.15;}
    .gs-price-modal span{font-size:13px;font-weight:600;color:#6B7280;margin-left:4px;}
    .gs-price-range{font-size:13.5px;color:#374151;margin:6px 0 8px;}
    .gs-price-meta{font-size:12.5px;color:#6B7280;line-height:1.5;}
    .gs-price-tag{
        display:inline-block;margin-top:9px;padding:3px 10px;border-radius:999px;
        font-size:11.5px;font-weight:700;background:#E8F5E9;color:#1B5E20;
    }
    .gs-price-tag.state{background:#FFF4E5;color:#8A5300;}
    .gs-price-empty-text{font-size:13.5px;color:#6B7280;margin-top:10px;}
    .gs-price-img{width:100%;height:125px;object-fit:cover;border-radius:11px;margin-bottom:10px;border:1px solid rgba(46,125,50,.12);background:#F3F7F3;}
    </style>
    """, unsafe_allow_html=True)

    st.title("📈 " + tr("market_title"))

    st.write(
        f"Live mandi prices for **{location}** from the Government of India "
        f"Open Government Data platform, data.gov.in."
    )

    key_col, refresh_col = st.columns([4, 1], vertical_alignment="bottom")
    with key_col:
        market_api_key = st.text_input(
            "🔑 data.gov.in API key",
            value=DEFAULT_MANDI_API_KEY,
            type="password",
            key="market_ui_api_key",
            help="Enter your free data.gov.in API key to load live mandi prices.",
        )
    with refresh_col:
        if st.button("🔄 Refresh", use_container_width=True, key="market_refresh_btn"):
            _fetch_state_records.clear()
            st.rerun()

    if not market_api_key.strip():
        st.info(
            "Enter your data.gov.in API key above to load live state mandi prices "
            f"for {location} ({district} district). No sample or simulated prices are shown on this page."
        )
    else:
        with st.spinner(f"Loading live mandi prices for {location}..."):
            results, error = get_mandi_prices(location, market_api_key.strip())

        available = [(c, r) for c, r in results if r]
        missing = [c for c, r in results if not r]
        crop_image_urls = get_crop_image_urls([c for c, _ in available] + missing)

        st.markdown(
            "<div class='gs-price-grid-note'>" + gs_fmt(
                "Showing {shown} of {total} crops, every vegetable priced individually, for "
                "<b>{location}</b>, {district} district • selected state/UT • prices in ₹ per quintal (100 kg)",
                shown=len(available), total=len(results),
                location=html.escape(tr_place(location)),
                district=html.escape(tr_place(location))) + "</div>",
            unsafe_allow_html=True
        )

        if error and not available:
            st.warning(error)

        if available:
            per_row = 3
            for start in range(0, len(available), per_row):
                chunk = available[start:start + per_row]
                cols = st.columns(per_row)
                for col, (crop, rec) in zip(cols, chunk):
                    scope = rec.get("scope")
                    if scope == "taluka":
                        tag_class = "gs-price-tag"
                        tag_text = f"{html.escape(str(location))} mandi"
                    elif scope == "district":
                        tag_class = "gs-price-tag"
                        tag_text = f"{html.escape(str(district))} district mandi"
                    else:
                        tag_class = "gs-price-tag state"
                        tag_text = "State mandi"
                    variety = str(rec.get("variety") or "").strip()
                    variety_line = (
                        f"<div class='gs-price-meta'>Variety: {html.escape(variety)}</div>"
                        if variety and variety.lower() not in ("other", "not reported")
                        else ""
                    )
                    with col:
                        st.markdown(
                            f"""<div class="gs-price-card">
  {f'<img class="gs-price-img" src="{html.escape(crop_image_urls.get(crop))}" alt="{html.escape(str(tr_data(crop)))}">' if crop_image_urls.get(crop) else ''}
  <div class="gs-price-crop">🌾 {html.escape(str(tr_data(crop)))}</div>
  <div class="gs-price-modal">₹{rec['modal']:,.0f}<span>/quintal</span></div>
  <div class="gs-price-range">Min ₹{rec['min']:,.0f} &nbsp;•&nbsp; Max ₹{rec['max']:,.0f}</div>
  <div class="gs-price-meta">Mandi: {html.escape(str(rec['market']))}</div>
  {variety_line}
  <div class="gs-price-meta">Arrival date: {html.escape(str(rec['date']))}</div>
  <div class="{tag_class}">{tag_text}</div>
</div>""",
                            unsafe_allow_html=True
                        )

        if missing:
            st.markdown("#### 🕒 No price reported today")
            per_row = 3
            for start in range(0, len(missing), per_row):
                chunk = missing[start:start + per_row]
                cols = st.columns(per_row)
                for col, crop in zip(cols, chunk):
                    with col:
                        st.markdown(
                            f"""<div class="gs-price-card empty">
  {f'<img class="gs-price-img" src="{html.escape(crop_image_urls.get(crop))}" alt="{html.escape(str(tr_data(crop)))}">' if crop_image_urls.get(crop) else ''}
  <div class="gs-price-crop">🌾 {html.escape(str(tr_data(crop)))}</div>
  <div class="gs-price-empty-text">No mandi price has been published for this
  crop in the latest available government update. Please check again later.</div>
</div>""",
                            unsafe_allow_html=True
                        )

        st.caption(
            "Source: Government of India • data.gov.in • Agmarknet daily mandi prices (Karnataka). "
            "Prices are the latest published records and may lag by a day or two. "
            "Verify at your local mandi before taking a financial decision."
        )

    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<div style='text-align:center; color:#5f6b78; font-size:14px;'>🌾 Gram Sahayak • Prototype for rural micro-entrepreneur business guidance</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; color:#667085; font-size:13px; margin-top:12px;'>Live state mandi prices • Rule-based recommendations • Verify official scheme information before decisions</div>", unsafe_allow_html=True)
    st.stop()

# Merge the user-provided records into the existing Government Schemes dataset.
# Existing entries from the same scheme family are removed first to avoid duplicate
# cards for KCC/PMEGP/PMMY/PMFME/AIF.
_SCHEME_FAMILY_KEYS = {
    "pm-kisan": "PM-KISAN",
    "kcc": "Kisan Credit Card",
    "mudra": "MUDRA",
    "pmegp": "PMEGP",
    "pmfme": "PMFME",
    "vishwakarma": "Vishwakarma",
    "aif": "Agriculture Infrastructure Fund",
}

def _scheme_family(name):
    n = name.lower()
    for key, family in _SCHEME_FAMILY_KEYS.items():
        if key in n:
            return family
    return name

_new_families = {_scheme_family(x["name"]) for x in GOVT_SCHEMES_DATA}
SCHEMES = [x for x in BASE_SCHEMES if _scheme_family(x["name"]) not in _new_families]
for _g in GOVT_SCHEMES_DATA:
    SCHEMES.append({
        "name": _g["name"],
        "best_for": _g["target"],
        "description": _g["benefit"],
        "key": _g["key_conditions"],
        "why": "Relevant when the applicant/business matches the scheme's stated beneficiary type, stage and activity conditions.",
        "source": _g["source_url"],
        "source_url": _g["source_url"],
        "documents": _g["documents"],
        "categories": _g["categories"],
        "beneficiary_types": _g["beneficiary_types"],
        "business_stages": _g["business_stages"],
        "funding_min": _g["funding_min"],
        "funding_max": _g["funding_max"],
        "keywords": _g["keywords"],
    })


# ------------------------------------------------------------
# GOVERNMENT SCHEME DISPLAY HELPERS
# ------------------------------------------------------------
# These helpers keep the Government Schemes renderer compatible
# with the translation system. They safely fall back to the
# original English text when a translation is not available.
def scheme_name(value):
    return tr_any(value)

def stext(kind, value):
    return tr_any(value)

def scheme_extra(kind, value):
    return tr_any(value)


if page == "Government Schemes":
    st.markdown(
        f"""<div class="gs-scheme-hero">
            <div class="gs-scheme-hero-icon">🏛️</div>
            <div>
                <div class="gs-eyebrow">GRAM SAHAYAK • SCHEME DISCOVERY</div>
                <h1>{html.escape(tr("scheme_title"))}</h1>
                <p>{html.escape(tr("scheme_desc"))}</p>
            </div>
        </div>""", unsafe_allow_html=True
    )

    all_beneficiaries = sorted({b for x in SCHEMES for b in x.get("beneficiary_types", [])})
    all_stages = sorted({b for x in SCHEMES for b in x.get("business_stages", [])})
    all_categories = sorted({b for x in SCHEMES for b in x.get("categories", [])})

    f1, f2, f3 = st.columns([1.05, 1.05, 1.05])
    with f1:
        beneficiary = st.selectbox("👤 " + tr_any("User / Beneficiary Type"), ["All"] + all_beneficiaries, key="scheme_beneficiary")
    with f2:
        stage = st.selectbox("🧭 " + tr_any("Business Stage"), ["All"] + all_stages, key="scheme_stage")
    with f3:
        category = st.selectbox("🌱 " + tr_any("Activity Category"), ["All"] + all_categories, key="scheme_category")

    f4, f5, f6 = st.columns([1.25, 1.0, 1.0])
    with f4:
        search = st.text_input("🔎 " + tr("search"), placeholder=tr("placeholder"), key="scheme_search")
    with f5:
        funding = st.number_input(
            "💰 " + tr_any("Approximate Funding Requirement (₹)"),
            min_value=0, max_value=20000000, value=100000, step=10000,
            key="scheme_funding"
        )
    with f6:
        st.markdown('<div class="gs-filter-spacer"></div>', unsafe_allow_html=True)
        matches_only = st.checkbox(tr_any("Show matches only (>30% profile match)"), value=False, key="scheme_matches")

    def scheme_profile_match(scheme):
        score = 0
        reasons = []
        max_score = 4
        if beneficiary == "All" or beneficiary in scheme.get("beneficiary_types", []):
            score += 1
            if beneficiary != "All":
                reasons.append("Beneficiary type aligns with the scheme profile.")
        if stage == "All" or stage in scheme.get("business_stages", []):
            score += 1
            if stage != "All":
                reasons.append("Business stage is covered by the scheme profile.")
        if category == "All" or category in scheme.get("categories", []):
            score += 1
            if category != "All":
                reasons.append("Activity category is covered by the scheme profile.")
        lo, hi = scheme.get("funding_min", 0), scheme.get("funding_max", 10**12)
        if lo == 0 and hi == 0:
            reasons.append("Funding amount is determined by the applicable scheme component, lender or current guidelines.")
        elif lo <= funding <= hi:
            score += 1
            reasons.append(f"Funding requirement (₹{funding:,.0f}) falls within the scheme range.")
        elif funding > 0:
            reasons.append(f"Funding requirement is outside the indicative range (₹{lo:,.0f} – ₹{hi:,.0f}).")
        return round(score / max_score * 100), reasons

    shown = []
    for scheme in SCHEMES:
        haystack = " ".join([
            scheme.get("name", ""), scheme.get("best_for", ""), scheme.get("description", ""),
            scheme.get("key", ""), scheme.get("why", ""),
            " ".join(scheme.get("keywords", [])), " ".join(scheme.get("categories", []))
        ]).lower()
        if search and search.lower().strip() not in haystack:
            continue
        match, reasons = scheme_profile_match(scheme)
        if matches_only and match <= 30:
            continue
        shown.append((scheme, match, reasons))

    shown.sort(key=lambda x: (-x[1], x[0].get("name", "")))
    total = len(SCHEMES)
    matched = sum(1 for _, m, _ in shown if m > 30)
    exact_range = sum(1 for x in SCHEMES if x.get("funding_min", 0) != 0 or x.get("funding_max", 0) != 0 if x.get("funding_min", 0) <= funding <= x.get("funding_max", 10**12))

    m1, m2, m3, m4 = st.columns(4)
    m1.markdown(f'<div class="gs-scheme-stat"><span>📋</span><strong>{len(shown)}</strong><small>{html.escape(tr_any("Schemes shown"))}</small></div>', unsafe_allow_html=True)
    m2.markdown(f'<div class="gs-scheme-stat"><span>🎯</span><strong>{matched}</strong><small>{html.escape(tr_any("Profile matches"))}</small></div>', unsafe_allow_html=True)
    m3.markdown(f'<div class="gs-scheme-stat"><span>💰</span><strong>{exact_range}</strong><small>{html.escape(tr_any("Funding range fit"))}</small></div>', unsafe_allow_html=True)
    m4.markdown(f'<div class="gs-scheme-stat"><span>🏛️</span><strong>{total}</strong><small>{html.escape(tr_any("Total schemes"))}</small></div>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="gs-match-note">ℹ️ {html.escape(tr_any("Matches are calculated programmatically for profile alignment. This is NOT an official eligibility confirmation."))}</div>',
        unsafe_allow_html=True
    )

    if not shown:
        st.info(tr_any("No schemes match the selected filters. Try changing the beneficiary, stage, category or funding requirement."))
    else:
        for idx, (scheme, match, reasons) in enumerate(shown, start=1):
            name = scheme_name(scheme.get("name", ""))
            benefit = stext("desc", scheme.get("description", ""))
            target = stext("best", scheme.get("best_for", ""))
            key_info = scheme_extra("key", scheme.get("key", ""))
            why = scheme_extra("why", scheme.get("why", ""))
            source_label = scheme_extra("source", scheme.get("source", ""))
            lo, hi = scheme.get("funding_min", 0), scheme.get("funding_max", 10**12)
            categories = scheme.get("categories", [])
            docs = scheme.get("documents", "")
            source_url = scheme.get("source_url") or scheme.get("source")
            match_class = "high" if match >= 75 else ("mid" if match > 30 else "low")
            badge_text = f"{match}% {tr_any('Profile Match')}"
            chips = "".join(f'<span class="gs-chip">{html.escape(str(c))}</span>' for c in categories[:4])
            reasons_html = "".join(f"<li>{html.escape(r)}</li>" for r in reasons)

            st.markdown(
                f"""<div class="gs-scheme-card gs-match-{match_class}">
                    <div class="gs-scheme-card-top">
                        <div class="gs-scheme-index">{idx:02d}</div>
                        <div class="gs-scheme-card-title">
                            <div class="gs-scheme-name">{html.escape(name)}</div>
                            <div class="gs-chip-row">{chips}</div>
                        </div>
                        <div class="gs-match-badge">🎯 {html.escape(badge_text)}</div>
                    </div>
                    <div class="gs-benefit-strip"><span>💡</span><div><b>{html.escape(tr_any('Key Benefit'))}</b><br>{html.escape(benefit)}</div></div>
                </div>""", unsafe_allow_html=True
            )

            if isinstance(source_url, str) and source_url.startswith("http"):
                official_html = f'<a href="{html.escape(source_url, quote=True)}" target="_blank" rel="noopener noreferrer">Visit Official Website ↗</a>'
            else:
                official_html = html.escape(str(source_label or "Not available"))

            funding_text = (
                f"Indicative range: ₹{lo:,.0f} – ₹{hi:,.0f}"
                if hi > 0 else
                "No direct funding amount specified; this is a market/trading portal."
            )
            table_rows = [
                ("🎯", "Purpose & Description", benefit),
                ("👥", "Target Beneficiaries", target),
                ("📋", "Major Eligibility Conditions", key_info),
                ("💰", "Financial Support / Range", funding_text),
                ("📄", "Important Documents Required", docs or "Check the official portal for current document requirements."),
                ("🔗", "Official Source / Portal", official_html),
            ]
            table_html = "".join(
                f'<tr><td class="gs-table-label"><span>{icon}</span><b>{html.escape(label)}</b></td><td>{value}</td></tr>'
                for icon, label, value in table_rows
            )
            st.markdown(
                f'<div class="gs-info-table-wrap"><table class="gs-info-table"><tbody>{table_html}</tbody></table></div>',
                unsafe_allow_html=True
            )

            if reasons:
                st.markdown(
                    f'<div class="gs-reason-box"><b>{html.escape(tr_any("Why this matches"))}</b><ul>{reasons_html}</ul></div>',
                    unsafe_allow_html=True
                )
            with st.expander(f"{tr_any('View scheme details')} · {name}"):
                st.markdown(f"**{tr_any('Why this scheme may be relevant')}:** {why}")
                st.markdown(f"**{tr_any('Profile alignment')}:** {match}%")
                if isinstance(source_url, str) and source_url.startswith("http"):
                    st.link_button("🔗 " + tr_any("Open Official Portal"), source_url)

    st.warning(tr("scheme_warning"))

# ============================================================
# FINANCIAL ASSISTANT
# ============================================================

# ============================================================
# PAGE 4: FINANCIAL ASSISTANT
# ============================================================
if page == "Financial Assistant":
    st.markdown(f"## 💰 {tr('finance_title')}")
    st.markdown(
        "Use these beginner-friendly calculators to plan business sales, "
        "evaluate loan EMIs, estimate affordability, and forecast monthly cash flows."
    )

    fin_tab1, fin_tab2, fin_tab3, fin_tab4 = st.tabs([
        tr("profit_tab"),
        tr("emi_tab"),
        "📊 Loan Affordability",
        "💵 Monthly Cash Flow Planner"
    ])

    # ========================================================
    # TAB 1: PROFIT CALCULATOR
    # ========================================================
    with fin_tab1:
        st.markdown(f"### {tr('profit_est')}")

        pc1, pc2 = st.columns(2)

        with pc1:
            fin_qty = st.number_input(
                tr("quantity"),
                min_value=1,
                value=100,
                step=10,
                key="fa_profit_qty"
            )

            fin_buy = st.number_input(
                tr("purchase"),
                min_value=0.0,
                value=20.0,
                step=1.0,
                key="fa_profit_buy"
            )

            fin_sell = st.number_input(
                tr("selling"),
                min_value=0.0,
                value=30.0,
                step=1.0,
                key="fa_profit_sell"
            )

        with pc2:
            fin_other = st.number_input(
                tr("other"),
                min_value=0.0,
                value=200.0,
                step=50.0,
                key="fa_profit_other"
            )

        # Calculations
        fin_total_purchase = fin_qty * fin_buy
        fin_total_cost = fin_total_purchase + fin_other
        fin_revenue = fin_qty * fin_sell
        fin_profit = fin_revenue - fin_total_cost

        # Profit margin
        fin_margin = (
            fin_profit / fin_revenue * 100
            if fin_revenue > 0
            else 0.0
        )

        # Break-even analysis
        unit_margin = fin_sell - fin_buy

        if unit_margin > 0:
            be_qty = math.ceil(fin_other / unit_margin)
            be_sales = be_qty * fin_sell
        else:
            be_qty = None
            be_sales = None

        st.divider()

        m1, m2, m3, m4 = st.columns(4)

        with m1:
            st.metric(
                tr("total_cost"),
                f"₹{fin_total_cost:,.2f}"
            )

        with m2:
            st.metric(
                tr("revenue"),
                f"₹{fin_revenue:,.2f}"
            )

        with m3:
            st.metric(
                tr("profit"),
                f"₹{fin_profit:,.2f}"
            )

        with m4:
            st.metric(
                "Profit Margin",
                f"{fin_margin:.1f}%"
            )

        if fin_profit > 0:
            st.success(f"✅ {tr('positive')}")

        elif abs(fin_profit) < 1e-5:
            st.info(f"⚖️ {tr('break_even')}")

        else:
            st.error(f"⚠️ {tr('loss')}")

        st.markdown("#### Break-Even Analysis")

        if unit_margin <= 0:
            st.warning(
                "Selling price per unit is less than or equal to "
                "purchase cost per unit. You cannot recover fixed/other "
                "costs at this price."
            )
        else:
            st.info(
                f"To cover your fixed/other costs of "
                f"**₹{fin_other:,.2f}**, you must sell at least "
                f"**{be_qty:,} units** "
                f"(total sales revenue of **₹{be_sales:,.2f}**)."
            )

    # ========================================================
    # TAB 2: LOAN EMI CALCULATOR
    # ========================================================
    with fin_tab2:
        st.markdown(f"### 🏦 {tr('loan')}")

        lc1, lc2 = st.columns(2)

        with lc1:
            fin_loan_amt = st.number_input(
                tr("loan"),
                min_value=1000,
                value=50000,
                step=1000,
                key="fa_emi_amt"
            )

            fin_rate = st.number_input(
                tr("rate"),
                min_value=0.0,
                max_value=30.0,
                value=9.0,
                step=0.5,
                key="fa_emi_rate"
            )

        with lc2:
            fin_years = st.number_input(
                tr("period"),
                min_value=1,
                max_value=20,
                value=3,
                step=1,
                key="fa_emi_years"
            )

        fin_n = fin_years * 12

        if fin_rate > 0:
            fin_r = (fin_rate / 100) / 12

            fin_emi = (
                fin_loan_amt
                * fin_r
                * ((1 + fin_r) ** fin_n)
            ) / (
                ((1 + fin_r) ** fin_n) - 1
            )

        else:
            fin_r = 0
            fin_emi = fin_loan_amt / fin_n

        fin_total_pay = fin_emi * fin_n
        fin_interest = fin_total_pay - fin_loan_amt

        st.divider()

        em1, em2, em3 = st.columns(3)

        with em1:
            st.metric(
                tr("monthly"),
                f"₹{fin_emi:,.2f}"
            )

        with em2:
            st.metric(
                tr("total_payment"),
                f"₹{fin_total_pay:,.2f}"
            )

        with em3:
            st.metric(
                tr("interest"),
                f"₹{fin_interest:,.2f}"
            )

        st.caption(f"💡 {tr('loan_note')}")

    # ========================================================
    # TAB 3: LOAN AFFORDABILITY CALCULATOR
    # ========================================================
    with fin_tab3:
        st.markdown("### 📊 Loan Affordability Calculator")

        st.markdown(
            "Enter the principal amount you want to borrow and your monthly "
            "income details to see whether the estimated EMI fits your budget."
        )

        ac1, ac2 = st.columns(2)

        with ac1:
            aff_principal = st.number_input(
                "Principal Amount / Loan Amount (₹)",
                min_value=1000.0,
                value=50000.0,
                step=1000.0,
                key="fa_aff_principal"
            )

            aff_income = st.number_input(
                "Monthly Income (₹)",
                min_value=0.0,
                value=30000.0,
                step=1000.0,
                key="fa_aff_income"
            )

            aff_living_exp = st.number_input(
                "Existing Monthly Living Expenses (₹)",
                min_value=0.0,
                value=15000.0,
                step=1000.0,
                key="fa_aff_living"
            )

        with ac2:
            aff_existing_emi = st.number_input(
                "Existing Monthly Loan EMIs (₹)",
                min_value=0.0,
                value=2000.0,
                step=500.0,
                key="fa_aff_emi"
            )

            aff_interest_rate = st.number_input(
                "Proposed Loan Interest Rate (% p.a.)",
                min_value=0.0,
                max_value=30.0,
                value=10.0,
                step=0.5,
                key="fa_aff_rate"
            )

            aff_period_years = st.number_input(
                "Proposed Loan Period (Years)",
                min_value=1,
                max_value=20,
                value=3,
                step=1,
                key="fa_aff_years"
            )

        # Simple affordability calculation
        aff_disposable_income = max(
            0.0,
            aff_income - aff_living_exp - aff_existing_emi
        )

        aff_n = aff_period_years * 12

        if aff_interest_rate > 0:
            aff_r = (aff_interest_rate / 100) / 12
            aff_emi = (
                aff_principal
                * aff_r
                * ((1 + aff_r) ** aff_n)
                / (((1 + aff_r) ** aff_n) - 1)
            )
        else:
            aff_emi = aff_principal / aff_n

        aff_total_payment = aff_emi * aff_n
        aff_total_interest = aff_total_payment - aff_principal

        if aff_disposable_income > 0:
            aff_emi_ratio = (aff_emi / aff_disposable_income) * 100
        else:
            aff_emi_ratio = float("inf")

        st.divider()

        am1, am2, am3, am4 = st.columns(4)

        with am1:
            st.metric(
                "Principal Amount",
                f"₹{aff_principal:,.2f}"
            )

        with am2:
            st.metric(
                "Estimated EMI",
                f"₹{aff_emi:,.2f}"
            )

        with am3:
            st.metric(
                "Available Monthly Income",
                f"₹{aff_disposable_income:,.2f}"
            )

        with am4:
            st.metric(
                "Total Interest",
                f"₹{aff_total_interest:,.2f}"
            )

        if aff_disposable_income <= 0:
            st.error(
                "⚠️ Your current income is fully used by the entered "
                "expenses and existing EMIs. The proposed loan EMI does "
                "not fit within the available monthly income."
            )
        elif aff_emi <= aff_disposable_income:
            st.success(
                f"✅ The estimated EMI of **₹{aff_emi:,.2f}** is within "
                f"your available monthly income of **₹{aff_disposable_income:,.2f}** "
                f"for the entered principal amount."
            )
        else:
            st.warning(
                f"⚠️ The estimated EMI of **₹{aff_emi:,.2f}** is higher "
                f"than your available monthly income of **₹{aff_disposable_income:,.2f}**."
            )

        st.info(
            f"📌 EMI uses the entered principal amount of **₹{aff_principal:,.2f}**, "
            f"an interest rate of **{aff_interest_rate:.1f}% p.a.**, and a "
            f"loan period of **{aff_period_years} years**."
        )

        st.caption(
            "ℹ️ This is a simple planning estimate. Actual loan eligibility, "
            "interest rates, fees and repayment terms depend on the lender."
        )

    # ========================================================
    # TAB 4: MONTHLY CASH FLOW PLANNER
    # ========================================================
    with fin_tab4:
        st.markdown("### 💵 Monthly Cash Flow Planner")

        st.markdown(
            "Plan your expected monthly income and expenses to "
            "estimate your remaining cash flow."
        )

        cf1, cf2 = st.columns(2)

        with cf1:
            cf_income = st.number_input(
                "Expected Monthly Business/Family Income (₹)",
                min_value=0.0,
                value=35000.0,
                step=1000.0,
                key="fa_cf_income"
            )

            cf_operating = st.number_input(
                "Monthly Operating / Business Expenses (₹)",
                min_value=0.0,
                value=12000.0,
                step=1000.0,
                key="fa_cf_operating"
            )

        with cf2:
            cf_household = st.number_input(
                "Monthly Household / Personal Expenses (₹)",
                min_value=0.0,
                value=14000.0,
                step=1000.0,
                key="fa_cf_household"
            )

            cf_emis = st.number_input(
                "Total Monthly Debt / EMI Payments (₹)",
                min_value=0.0,
                value=3000.0,
                step=500.0,
                key="fa_cf_emis"
            )

        # Cash flow calculation
        cf_total_expenses = (
            cf_operating
            + cf_household
            + cf_emis
        )

        cf_net_cash_flow = (
            cf_income
            - cf_total_expenses
        )

        st.divider()

        cfm1, cfm2, cfm3 = st.columns(3)

        with cfm1:
            st.metric(
                "Total Monthly Income",
                f"₹{cf_income:,.2f}"
            )

        with cfm2:
            st.metric(
                "Total Monthly Expenses",
                f"₹{cf_total_expenses:,.2f}"
            )

        with cfm3:
            st.metric(
                "Remaining Cash Flow",
                f"₹{cf_net_cash_flow:,.2f}"
            )

        if cf_net_cash_flow > 0:

            st.success(
                f"✅ **Positive Cash Flow:** "
                f"₹{cf_net_cash_flow:,.2f} remains after "
                f"the entered monthly expenses and EMIs."
            )

        elif abs(cf_net_cash_flow) < 1e-5:

            st.info(
                "⚖️ **Zero Cash Flow:** Your entered monthly "
                "income exactly covers your expenses and EMIs."
            )

        else:

            st.error(
                f"⚠️ **Negative Cash Flow:** Your monthly deficit "
                f"is **₹{abs(cf_net_cash_flow):,.2f}** based on "
                f"the entered values."
            )

    st.markdown("<br>", unsafe_allow_html=True)

    st.warning(
        "⚠️ **Financial Safety Note:** All calculations provided "
        "in this section are estimates for guidance and educational "
        "planning. Actual bank interest rates, repayment schedules, "
        "and loan eligibility decisions depend on official lender policies."
    )

# DOMAIN-BASED BUSINESS RECOMMENDATION CONFIGURATION
# ============================================================
# Each business has its own inputs, requirement checks, weights and risks.
# Numeric financial fields are only shown when supported by the existing
# business profile; otherwise the app explicitly marks them as unavailable.

BUSINESS_DOMAIN_CONFIG = {
    "Agriculture": {
        "icon": "🌾",
        "businesses": {
            "Crop Cultivation": {
                "inputs": [
                    ("land_acres", "Land area (acres)", "number", {"min_value": 0.5, "value": 1.0, "step": 0.5}),
                    ("season", "Season", "select", {"options": ["Kharif", "Rabi", "Summer"]}),
                    ("water", "Water availability", "select", {"options": ["None", "Low", "Medium", "High"]}),
                    ("irrigation", "Irrigation", "select", {"options": ["Rain-fed", "Limited", "Available", "Reliable"]}),
                    ("soil_test", "Soil test available", "select", {"options": ["Yes", "No"]}),
                    ("labour", "Available labour (people)", "number", {"min_value": 0, "value": 1, "step": 1}),
                    ("investment", "Available investment (₹)", "number", {"min_value": 0, "value": 100000, "step": 5000}),
                    ("market_access", "Market access", "select", {"options": ["Poor", "Moderate", "Good"]}),
                    ("income_time", "Target time to income", "select", {"options": ["Within 3 months", "3–6 months", "6–12 months", "12+ months"]}),
                    ("risk", "Risk preference", "select", {"options": ["Low", "Medium", "High"]}),
                ],
                "requirements": {"Water": "Water suitable for the chosen crop/season", "Land": "Sufficient cultivable land", "Market": "A practical selling channel", "Soil": "Soil information is strongly recommended"},
                "weights": {"land_acres": 15, "season": 10, "water": 12, "irrigation": 8, "soil_test": 8, "labour": 7, "investment": 15, "market_access": 12, "income_time": 6, "risk": 7},
                "risks": ["Weather variability", "Water availability", "Input-price changes", "Crop-price changes", "Pest/disease pressure"],
            },
            "Cereals": {
                "inputs": [],
                "requirements": {},
                "weights": {},
                "risks": ["Weather variability", "Water availability", "Input-price changes", "Market-price changes", "Pest/disease pressure"],
            },
            "Pulses": {
                "inputs": [],
                "requirements": {},
                "weights": {},
                "risks": ["Rainfall variability", "Pest/disease pressure", "Input-price changes", "Market-price changes"],
            },
            "Oilseeds": {
                "inputs": [],
                "requirements": {},
                "weights": {},
                "risks": ["Weather variability", "Water stress", "Pest/disease pressure", "Market-price changes"],
            },
            "Commercial Crops": {
                "inputs": [],
                "requirements": {},
                "weights": {},
                "risks": ["Longer production cycle", "Input-price changes", "Market-price changes", "Weather variability"],
            },
            "Vegetable Cultivation": {
                "inputs": [
                    ("land_acres", "Land area (acres)", "number", {"min_value": 0.5, "value": 1.0, "step": 0.5}),
                    ("season", "Season", "select", {"options": ["Kharif", "Rabi", "Summer"]}),
                    ("water", "Water availability", "select", {"options": ["None", "Low", "Medium", "High"]}),
                    ("irrigation", "Irrigation", "select", {"options": ["Rain-fed", "Limited", "Available", "Reliable"]}),
                    ("soil_test", "Soil test available", "select", {"options": ["Yes", "No"]}),
                    ("labour", "Available labour (people)", "number", {"min_value": 0, "value": 2, "step": 1}),
                    ("investment", "Available investment (₹)", "number", {"min_value": 0, "value": 100000, "step": 5000}),
                    ("market_access", "Market access", "select", {"options": ["Poor", "Moderate", "Good"]}),
                    ("transport", "Transport available", "select", {"options": ["No", "Shared", "Yes"]}),
                    ("income_time", "Target time to income", "select", {"options": ["Within 3 months", "3–6 months", "6–12 months"]}),
                ],
                "requirements": {"Water": "Reliable water is important for vegetable production", "Labour": "Regular crop-care labour", "Market": "Fast access to a selling channel", "Transport": "Useful for frequent harvest movement"},
                "weights": {"land_acres": 12, "water": 15, "irrigation": 10, "soil_test": 6, "labour": 10, "investment": 13, "market_access": 15, "transport": 8, "income_time": 6, "season": 5},
                "risks": ["Perishability", "Price fluctuations", "Pest/disease pressure", "Water stress"],
            },
            "Fruit Cultivation": {
                "inputs": [
                    ("land_acres", "Land area (acres)", "number", {"min_value": 0.5, "value": 1.0, "step": 0.5}),
                    ("water", "Water availability", "select", {"options": ["None", "Low", "Medium", "High"]}),
                    ("irrigation", "Irrigation", "select", {"options": ["Rain-fed", "Limited", "Available", "Reliable"]}),
                    ("soil_test", "Soil test available", "select", {"options": ["Yes", "No"]}),
                    ("labour", "Available labour (people)", "number", {"min_value": 0, "value": 2, "step": 1}),
                    ("investment", "Available investment (₹)", "number", {"min_value": 0, "value": 150000, "step": 5000}),
                    ("market_access", "Market access", "select", {"options": ["Poor", "Moderate", "Good"]}),
                    ("storage", "Storage available", "select", {"options": ["No", "Partial", "Yes"]}),
                    ("long_term", "Can wait for longer establishment period", "select", {"options": ["No", "Yes"]}),
                ],
                "requirements": {"Land": "Sufficient land for orchard layout", "Water": "Long-term water availability", "Capital": "Higher upfront establishment cost", "Time": "Ability to wait for orchard establishment"},
                "weights": {"land_acres": 15, "water": 15, "irrigation": 10, "soil_test": 7, "labour": 8, "investment": 18, "market_access": 10, "storage": 5, "long_term": 12},
                "risks": ["Long establishment period", "Weather extremes", "Pest/disease pressure", "Market-price variability"],
            },
            "Spice Cultivation": {
                "inputs": [
                    ("land_acres", "Land area (acres)", "number", {"min_value": 0.5, "value": 1.0, "step": 0.5}),
                    ("season", "Season", "select", {"options": ["Kharif", "Rabi", "Summer"]}),
                    ("water", "Water availability", "select", {"options": ["None", "Low", "Medium", "High"]}),
                    ("soil_test", "Soil test available", "select", {"options": ["Yes", "No"]}),
                    ("labour", "Available labour (people)", "number", {"min_value": 0, "value": 2, "step": 1}),
                    ("investment", "Available investment (₹)", "number", {"min_value": 0, "value": 100000, "step": 5000}),
                    ("market_access", "Market access", "select", {"options": ["Poor", "Moderate", "Good"]}),
                    ("drying", "Drying/processing space", "select", {"options": ["No", "Partial", "Yes"]}),
                    ("income_time", "Target time to income", "select", {"options": ["Within 3 months", "3–6 months", "6–12 months", "12+ months"]}),
                ],
                "requirements": {"Water": "Crop-specific water requirement", "Labour": "Regular crop management", "Processing": "Post-harvest drying/handling may be required", "Market": "Quality-sensitive buyers"},
                "weights": {"land_acres": 12, "season": 8, "water": 12, "soil_test": 8, "labour": 10, "investment": 13, "market_access": 15, "drying": 10, "income_time": 12},
                "risks": ["Quality variation", "Price volatility", "Pest/disease pressure", "Post-harvest loss"],
            },
            "Floriculture": {
                "inputs": [
                    ("land_acres", "Land/covered area (acres)", "number", {"min_value": 0.5, "value": 0.5, "step": 0.5}),
                    ("water", "Water availability", "select", {"options": ["None", "Low", "Medium", "High"]}),
                    ("irrigation", "Irrigation", "select", {"options": ["Rain-fed", "Limited", "Available", "Reliable"]}),
                    ("labour", "Available labour (people)", "number", {"min_value": 0, "value": 2, "step": 1}),
                    ("investment", "Available investment (₹)", "number", {"min_value": 0, "value": 100000, "step": 5000}),
                    ("market_access", "Market access", "select", {"options": ["Poor", "Moderate", "Good"]}),
                    ("transport", "Transport available", "select", {"options": ["No", "Shared", "Yes"]}),
                    ("protected", "Protected cultivation/structure available", "select", {"options": ["No", "Partial", "Yes"]}),
                ],
                "requirements": {"Water": "Reliable irrigation", "Labour": "Regular harvesting/handling", "Market": "Fast access to buyers", "Transport": "Important because flowers are perishable"},
                "weights": {"land_acres": 10, "water": 15, "irrigation": 10, "labour": 12, "investment": 16, "market_access": 15, "transport": 12, "protected": 10},
                "risks": ["High perishability", "Demand fluctuations", "Weather sensitivity", "Post-harvest handling"],
            },
        }
    },
    "Livestock": {
        "icon": "🐄",
        "businesses": {
            "Poultry Farming": {
                "inputs": [
                    ("birds", "Number of birds planned", "number", {"min_value": 1, "value": 500, "step": 50}),
                    ("shed", "Suitable shed available", "select", {"options": ["No", "Partial", "Yes"]}),
                    ("shed_area", "Available shed area (sq ft)", "number", {"min_value": 0, "value": 500, "step": 50}),
                    ("water", "Water availability", "select", {"options": ["None", "Low", "Medium", "High"]}),
                    ("feed", "Feed availability", "select", {"options": ["Poor", "Moderate", "Good"]}),
                    ("electricity", "Electricity", "select", {"options": ["No", "Limited", "Reliable"]}),
                    ("labour", "Available labour (people)", "number", {"min_value": 0, "value": 1, "step": 1}),
                    ("investment", "Available investment (₹)", "number", {"min_value": 0, "value": 150000, "step": 5000}),
                    ("veterinary", "Veterinary support access", "select", {"options": ["No", "Limited", "Good"]}),
                    ("market_access", "Market access", "select", {"options": ["Poor", "Moderate", "Good"]}),
                    ("experience", "Experience", "select", {"options": ["Beginner", "Some experience", "Experienced"]}),
                    ("income_time", "Target time to income", "select", {"options": ["Within 3 months", "3–6 months", "6–12 months"]}),
                ],
                "requirements": {"Housing": "Suitable, ventilated poultry housing", "Water": "Reliable clean water", "Feed": "Reliable feed supply", "Health": "Veterinary/vaccination arrangement", "Market": "Buyer/market access"},
                "weights": {"birds": 5, "shed": 10, "shed_area": 7, "water": 10, "feed": 10, "electricity": 5, "labour": 6, "investment": 15, "veterinary": 12, "market_access": 10, "experience": 5, "income_time": 5},
                "risks": ["Disease and mortality", "Feed-cost changes", "Market-price changes", "Heat/stress management", "Biosecurity failures"],
            },
            "Dairy Farming": {
                "inputs": [
                    ("animals", "Number of animals planned", "number", {"min_value": 1, "value": 2, "step": 1}),
                    ("animal_type", "Animal type", "select", {"options": ["Cows", "Buffaloes", "Mixed"]}),
                    ("shed", "Suitable shed available", "select", {"options": ["No", "Partial", "Yes"]}),
                    ("fodder", "Fodder availability", "select", {"options": ["Poor", "Moderate", "Good"]}),
                    ("water", "Water availability", "select", {"options": ["None", "Low", "Medium", "High"]}),
                    ("veterinary", "Veterinary support access", "select", {"options": ["No", "Limited", "Good"]}),
                    ("equipment", "Milking/chilling equipment", "select", {"options": ["No", "Partial", "Yes"]}),
                    ("labour", "Available labour (people)", "number", {"min_value": 0, "value": 1, "step": 1}),
                    ("investment", "Available investment (₹)", "number", {"min_value": 0, "value": 200000, "step": 5000}),
                    ("market_access", "Milk market access", "select", {"options": ["Poor", "Moderate", "Good"]}),
                    ("experience", "Experience", "select", {"options": ["Beginner", "Some experience", "Experienced"]}),
                ],
                "requirements": {"Housing": "Animal shed", "Feed": "Reliable fodder", "Water": "Adequate drinking/cleaning water", "Health": "Veterinary support", "Market": "Milk buyer/collection channel"},
                "weights": {"animals": 5, "animal_type": 4, "shed": 10, "fodder": 12, "water": 10, "veterinary": 10, "equipment": 5, "labour": 6, "investment": 15, "market_access": 12, "experience": 7, "income_time": 4},
                "risks": ["Animal disease", "Feed/fodder cost", "Milk-price variation", "Water shortage", "Animal productivity variation"],
            },
            "Goat Farming": {
                "inputs": [
                    ("animals", "Number of goats planned", "number", {"min_value": 1, "value": 10, "step": 1}),
                    ("shed", "Goat shed available", "select", {"options": ["No", "Partial", "Yes"]}),
                    ("grazing", "Grazing/feed availability", "select", {"options": ["Poor", "Moderate", "Good"]}),
                    ("water", "Water availability", "select", {"options": ["None", "Low", "Medium", "High"]}),
                    ("veterinary", "Veterinary support access", "select", {"options": ["No", "Limited", "Good"]}),
                    ("labour", "Available labour (people)", "number", {"min_value": 0, "value": 1, "step": 1}),
                    ("investment", "Available investment (₹)", "number", {"min_value": 0, "value": 150000, "step": 5000}),
                    ("market_access", "Market access", "select", {"options": ["Poor", "Moderate", "Good"]}),
                    ("experience", "Experience", "select", {"options": ["Beginner", "Some experience", "Experienced"]}),
                ],
                "requirements": {"Housing": "Dry, secure shelter", "Feed": "Grazing or feed supply", "Water": "Regular clean water", "Health": "Veterinary access", "Market": "Livestock buyer access"},
                "weights": {"animals": 7, "shed": 10, "grazing": 14, "water": 10, "veterinary": 10, "labour": 8, "investment": 15, "market_access": 12, "experience": 8, "season": 6},
                "risks": ["Disease", "Feed availability", "Market-price variation", "Mortality", "Predation/security"],
            },
            "Sheep Farming": {
                "inputs": [
                    ("animals", "Number of sheep planned", "number", {"min_value": 1, "value": 10, "step": 1}),
                    ("shed", "Sheep shed available", "select", {"options": ["No", "Partial", "Yes"]}),
                    ("grazing", "Grazing/feed availability", "select", {"options": ["Poor", "Moderate", "Good"]}),
                    ("water", "Water availability", "select", {"options": ["None", "Low", "Medium", "High"]}),
                    ("veterinary", "Veterinary support access", "select", {"options": ["No", "Limited", "Good"]}),
                    ("labour", "Available labour (people)", "number", {"min_value": 0, "value": 1, "step": 1}),
                    ("investment", "Available investment (₹)", "number", {"min_value": 0, "value": 150000, "step": 5000}),
                    ("market_access", "Market access", "select", {"options": ["Poor", "Moderate", "Good"]}),
                    ("experience", "Experience", "select", {"options": ["Beginner", "Some experience", "Experienced"]}),
                ],
                "requirements": {"Housing": "Dry secure shelter", "Feed": "Grazing/feed supply", "Water": "Regular clean water", "Health": "Veterinary access", "Market": "Buyer access"},
                "weights": {"animals": 7, "shed": 10, "grazing": 14, "water": 10, "veterinary": 10, "labour": 8, "investment": 15, "market_access": 12, "experience": 8, "season": 6},
                "risks": ["Disease", "Feed shortage", "Market-price variation", "Mortality", "Predation/security"],
            },
        }
    },
    "Aquaculture": {
        "icon": "🐟",
        "businesses": {
            "Fish Farming": {
                "inputs": [
                    ("pond_area", "Pond area (acres)", "number", {"min_value": 0.05, "value": 0.5}),
                    ("pond_type", "Pond type", "select", {"options": ["Existing pond", "New pond", "Lined pond", "Other"]}),
                    ("water_source", "Water source", "select", {"options": ["Rain-fed", "Canal", "Borewell", "Tank/Pond", "River", "Other"]}),
                    ("water_quality", "Water quality assessment", "select", {"options": ["Unknown", "Poor", "Moderate", "Good"]}),
                    ("water_availability", "Water availability", "select", {"options": ["Seasonal", "Perennial"]}),
                    ("species", "Fish species selected", "text", {}),
                    ("feed", "Feed availability", "select", {"options": ["Poor", "Moderate", "Good"]}),
                    ("electricity", "Electricity", "select", {"options": ["No", "Limited", "Reliable"]}),
                    ("labour", "Available labour (people)", "number", {"min_value": 0, "value": 1, "step": 1}),
                    ("investment", "Available investment (₹)", "number", {"min_value": 0, "value": 200000, "step": 5000}),
                    ("market_access", "Market access", "select", {"options": ["Poor", "Moderate", "Good"]}),
                    ("experience", "Experience", "select", {"options": ["Beginner", "Some experience", "Experienced"]}),
                ],
                "requirements": {"Pond": "Adequate pond area and suitable infrastructure", "Water quality": "Suitable water quality", "Water": "Stable water availability", "Feed": "Reliable feed supply", "Market": "Buyer/market channel"},
                "weights": {"pond_area": 15, "pond_type": 6, "water_source": 8, "water_quality": 15, "water_availability": 10, "species": 3, "feed": 10, "electricity": 5, "labour": 6, "investment": 12, "market_access": 7, "experience": 3},
                "risks": ["Water-quality failure", "Disease", "Feed costs", "Fish mortality", "Market-price changes"],
            },
        }
    },
    "Horticulture & Nursery": {
        "icon": "🌱",
        "businesses": {
            "Plant Nursery": {
                "inputs": [("space", "Nursery space (sq ft)", "number", {"min_value": 10, "value": 1000, "step": 50}), ("water", "Water availability", "select", {"options": ["None", "Low", "Medium", "High"]}), ("irrigation", "Irrigation", "select", {"options": ["None", "Limited", "Available", "Reliable"]}), ("shade", "Shade/protected area", "select", {"options": ["No", "Partial", "Yes"]}), ("plant_material", "Planting material source", "select", {"options": ["Poor", "Moderate", "Reliable"]}), ("labour", "Available labour (people)", "number", {"min_value": 0, "value": 1, "step": 1}), ("investment", "Available investment (₹)", "number", {"min_value": 0, "value": 100000, "step": 5000}), ("market_access", "Market access", "select", {"options": ["Poor", "Moderate", "Good"]}), ("transport", "Transport available", "select", {"options": ["No", "Shared", "Yes"]})],
                "requirements": {"Space": "Nursery area", "Water": "Reliable watering", "Plant material": "Consistent source", "Market": "Local buyer demand"},
                "weights": {"space": 12, "water": 14, "irrigation": 10, "shade": 10, "plant_material": 12, "labour": 8, "investment": 14, "market_access": 12, "transport": 8},
                "risks": ["Plant mortality", "Seasonal demand", "Water stress", "Disease/pest pressure"],
            },
            "Fruit Nursery": {
                "inputs": [("space", "Nursery space (sq ft)", "number", {"min_value": 10, "value": 1500, "step": 50}), ("water", "Water availability", "select", {"options": ["None", "Low", "Medium", "High"]}), ("shade", "Shade/protected area", "select", {"options": ["No", "Partial", "Yes"]}), ("plant_material", "Certified/quality planting material access", "select", {"options": ["Poor", "Moderate", "Reliable"]}), ("labour", "Available labour (people)", "number", {"min_value": 0, "value": 1, "step": 1}), ("investment", "Available investment (₹)", "number", {"min_value": 0, "value": 150000, "step": 5000}), ("market_access", "Market access", "select", {"options": ["Poor", "Moderate", "Good"]}), ("transport", "Transport available", "select", {"options": ["No", "Shared", "Yes"]})],
                "requirements": {"Space": "Nursery space", "Water": "Regular watering", "Plant material": "Quality planting material", "Market": "Demand from growers"},
                "weights": {"space": 13, "water": 14, "shade": 10, "plant_material": 16, "labour": 8, "investment": 15, "market_access": 14, "transport": 10},
                "risks": ["Plant-quality issues", "Demand variability", "Water stress", "Disease"],
            },
            "Flower Nursery": {
                "inputs": [("space", "Nursery space (sq ft)", "number", {"min_value": 10, "value": 1000, "step": 50}), ("water", "Water availability", "select", {"options": ["None", "Low", "Medium", "High"]}), ("shade", "Shade/protected area", "select", {"options": ["No", "Partial", "Yes"]}), ("labour", "Available labour (people)", "number", {"min_value": 0, "value": 2, "step": 1}), ("investment", "Available investment (₹)", "number", {"min_value": 0, "value": 100000, "step": 5000}), ("market_access", "Market access", "select", {"options": ["Poor", "Moderate", "Good"]}), ("transport", "Transport available", "select", {"options": ["No", "Shared", "Yes"]})],
                "requirements": {"Space": "Nursery/production space", "Water": "Regular watering", "Market": "Local demand and transport"},
                "weights": {"space": 13, "water": 15, "shade": 12, "labour": 10, "investment": 15, "market_access": 18, "transport": 17},
                "risks": ["Perishability", "Seasonal demand", "Disease", "Transport damage"],
            },
        }
    },
    "Allied Activities": {
        "icon": "🐝",
        "businesses": {
            "Beekeeping": {
                "inputs": [("boxes", "Bee boxes planned", "number", {"min_value": 1, "value": 10, "step": 1}), ("forage", "Flowering/forage availability", "select", {"options": ["Poor", "Moderate", "Good"]}), ("water", "Water availability", "select", {"options": ["None", "Low", "Medium", "High"]}), ("equipment", "Beekeeping equipment", "select", {"options": ["No", "Partial", "Yes"]}), ("labour", "Available labour (people)", "number", {"min_value": 0, "value": 1, "step": 1}), ("investment", "Available investment (₹)", "number", {"min_value": 0, "value": 100000, "step": 5000}), ("market_access", "Market access", "select", {"options": ["Poor", "Moderate", "Good"]}), ("experience", "Experience", "select", {"options": ["Beginner", "Some experience", "Experienced"]})],
                "requirements": {"Forage": "Adequate flowering/forage source", "Equipment": "Bee boxes and handling equipment", "Market": "Honey/wax selling channel"},
                "weights": {"boxes": 10, "forage": 20, "water": 6, "equipment": 15, "labour": 8, "investment": 15, "market_access": 16, "experience": 10},
                "risks": ["Colony loss", "Weather", "Pests/disease", "Market-price variation"],
            },
            "Mushroom Cultivation": {
                "inputs": [("room_area", "Growing room area (sq ft)", "number", {"min_value": 10, "value": 500, "step": 25}), ("temperature_control", "Temperature control", "select", {"options": ["No", "Partial", "Yes"]}), ("humidity_control", "Humidity control", "select", {"options": ["No", "Partial", "Yes"]}), ("water", "Water availability", "select", {"options": ["None", "Low", "Medium", "High"]}), ("substrate", "Substrate/raw material availability", "select", {"options": ["Poor", "Moderate", "Good"]}), ("electricity", "Electricity", "select", {"options": ["No", "Limited", "Reliable"]}), ("labour", "Available labour (people)", "number", {"min_value": 0, "value": 1, "step": 1}), ("investment", "Available investment (₹)", "number", {"min_value": 0, "value": 100000, "step": 5000}), ("market_access", "Market access", "select", {"options": ["Poor", "Moderate", "Good"]})],
                "requirements": {"Growing space": "Suitable clean growing space", "Environment": "Temperature/humidity management", "Water": "Reliable water", "Market": "Fast selling channel"},
                "weights": {"room_area": 12, "temperature_control": 14, "humidity_control": 14, "water": 10, "substrate": 12, "electricity": 8, "labour": 7, "investment": 11, "market_access": 12},
                "risks": ["Contamination", "Temperature/humidity fluctuations", "Short shelf life", "Market demand"],
            },
            "Sericulture": {
                "inputs": [("mulberry_land", "Mulberry area (acres)", "number", {"min_value": 0.1, "value": 1.0}), ("water", "Water availability", "select", {"options": ["None", "Low", "Medium", "High"]}), ("rearing_space", "Rearing space", "select", {"options": ["No", "Partial", "Yes"]}), ("labour", "Available labour (people)", "number", {"min_value": 0, "value": 2, "step": 1}), ("investment", "Available investment (₹)", "number", {"min_value": 0, "value": 150000, "step": 5000}), ("market_access", "Market access", "select", {"options": ["Poor", "Moderate", "Good"]}), ("experience", "Experience", "select", {"options": ["Beginner", "Some experience", "Experienced"]})],
                "requirements": {"Mulberry": "Mulberry cultivation/source", "Water": "Regular water", "Rearing": "Suitable rearing space", "Market": "Cocoon/market channel"},
                "weights": {"mulberry_land": 16, "water": 15, "rearing_space": 14, "labour": 12, "investment": 16, "market_access": 17, "experience": 10},
                "risks": ["Disease", "Weather", "Leaf availability", "Market-price variation"],
            },
        }
    },
    "Agri/Food Processing": {
        "icon": "🏭",
        "businesses": {
            "Grain Milling": {
                "inputs": [("workspace", "Workspace available", "select", {"options": ["No", "Partial", "Yes"]}), ("raw_material", "Raw-material availability", "select", {"options": ["Poor", "Moderate", "Good"]}), ("machine", "Milling machine available", "select", {"options": ["No", "Partial", "Yes"]}), ("electricity", "Electricity", "select", {"options": ["No", "Limited", "Reliable"]}), ("labour", "Available labour (people)", "number", {"min_value": 0, "value": 2, "step": 1}), ("investment", "Available investment (₹)", "number", {"min_value": 0, "value": 300000, "step": 10000}), ("storage", "Storage available", "select", {"options": ["No", "Partial", "Yes"]}), ("market_access", "Market access", "select", {"options": ["Poor", "Moderate", "Good"]})],
                "requirements": {"Workspace": "Food-grade workspace", "Raw material": "Reliable grain supply", "Machine": "Suitable milling equipment", "Electricity": "Reliable power", "Market": "Local selling channel"},
                "weights": {"workspace": 10, "raw_material": 17, "machine": 16, "electricity": 10, "labour": 8, "investment": 15, "storage": 10, "market_access": 14},
                "risks": ["Raw-material price", "Machine downtime", "Electricity interruptions", "Competition"],
            },
            "Spice Processing": {
                "inputs": [("workspace", "Workspace available", "select", {"options": ["No", "Partial", "Yes"]}), ("raw_material", "Raw-material availability", "select", {"options": ["Poor", "Moderate", "Good"]}), ("grinder", "Grinding/processing equipment", "select", {"options": ["No", "Partial", "Yes"]}), ("electricity", "Electricity", "select", {"options": ["No", "Limited", "Reliable"]}), ("labour", "Available labour (people)", "number", {"min_value": 0, "value": 2, "step": 1}), ("investment", "Available investment (₹)", "number", {"min_value": 0, "value": 250000, "step": 10000}), ("packaging", "Packaging availability", "select", {"options": ["Poor", "Moderate", "Good"]}), ("market_access", "Market access", "select", {"options": ["Poor", "Moderate", "Good"]})],
                "requirements": {"Workspace": "Clean processing area", "Raw material": "Reliable spice supply", "Equipment": "Grinding/packing equipment", "Packaging": "Suitable packaging", "Market": "Retail/wholesale buyers"},
                "weights": {"workspace": 10, "raw_material": 18, "grinder": 15, "electricity": 8, "labour": 8, "investment": 15, "packaging": 12, "market_access": 14},
                "risks": ["Raw-material quality", "Food safety requirements", "Packaging cost", "Competition"],
            },
            "Oil Extraction": {
                "inputs": [("workspace", "Workspace available", "select", {"options": ["No", "Partial", "Yes"]}), ("oilseed_supply", "Oilseed availability", "select", {"options": ["Poor", "Moderate", "Good"]}), ("machine", "Oil extraction machine", "select", {"options": ["No", "Partial", "Yes"]}), ("electricity", "Electricity", "select", {"options": ["No", "Limited", "Reliable"]}), ("labour", "Available labour (people)", "number", {"min_value": 0, "value": 2, "step": 1}), ("investment", "Available investment (₹)", "number", {"min_value": 0, "value": 400000, "step": 10000}), ("storage", "Storage available", "select", {"options": ["No", "Partial", "Yes"]}), ("market_access", "Market access", "select", {"options": ["Poor", "Moderate", "Good"]})],
                "requirements": {"Raw material": "Steady oilseed supply", "Machine": "Suitable extraction unit", "Electricity": "Reliable power", "Storage": "Safe storage", "Market": "Retail/wholesale market"},
                "weights": {"workspace": 8, "oilseed_supply": 18, "machine": 18, "electricity": 10, "labour": 7, "investment": 16, "storage": 8, "market_access": 15},
                "risks": ["Oilseed price", "Equipment downtime", "Quality compliance", "Competition"],
            },
            "Pickle / Jam / Food Processing": {
                "inputs": [("workspace", "Food-processing workspace", "select", {"options": ["No", "Partial", "Yes"]}), ("raw_material", "Raw-material availability", "select", {"options": ["Poor", "Moderate", "Good"]}), ("equipment", "Processing equipment", "select", {"options": ["No", "Partial", "Yes"]}), ("electricity", "Electricity", "select", {"options": ["No", "Limited", "Reliable"]}), ("labour", "Available labour (people)", "number", {"min_value": 0, "value": 2, "step": 1}), ("investment", "Available investment (₹)", "number", {"min_value": 0, "value": 150000, "step": 5000}), ("packaging", "Packaging availability", "select", {"options": ["Poor", "Moderate", "Good"]}), ("market_access", "Market access", "select", {"options": ["Poor", "Moderate", "Good"]}), ("storage", "Storage available", "select", {"options": ["No", "Partial", "Yes"]})],
                "requirements": {"Workspace": "Clean food-processing space", "Raw material": "Seasonal/local raw material", "Packaging": "Food-grade packaging", "Market": "Local retail or direct customers"},
                "weights": {"workspace": 12, "raw_material": 16, "equipment": 12, "electricity": 8, "labour": 8, "investment": 15, "packaging": 12, "market_access": 12, "storage": 5},
                "risks": ["Food spoilage", "Raw-material seasonality", "Food safety requirements", "Demand variability"],
            },
            "Milk Processing": {
                "inputs": [("milk_supply", "Milk supply availability", "select", {"options": ["Poor", "Moderate", "Good"]}), ("workspace", "Processing workspace", "select", {"options": ["No", "Partial", "Yes"]}), ("equipment", "Processing equipment", "select", {"options": ["No", "Partial", "Yes"]}), ("electricity", "Electricity", "select", {"options": ["No", "Limited", "Reliable"]}), ("cold_storage", "Cold storage/refrigeration", "select", {"options": ["No", "Partial", "Yes"]}), ("labour", "Available labour (people)", "number", {"min_value": 0, "value": 2, "step": 1}), ("investment", "Available investment (₹)", "number", {"min_value": 0, "value": 250000, "step": 10000}), ("market_access", "Market access", "select", {"options": ["Poor", "Moderate", "Good"]})],
                "requirements": {"Milk": "Reliable milk supply", "Workspace": "Clean processing area", "Cold chain": "Adequate chilling/storage", "Market": "Buyer network"},
                "weights": {"milk_supply": 20, "workspace": 10, "equipment": 15, "electricity": 10, "cold_storage": 15, "labour": 8, "investment": 10, "market_access": 12},
                "risks": ["Perishability", "Cold-chain failure", "Milk quality variation", "Food safety requirements"],
            },
        }
    },
    "Farm Services": {
        "icon": "🚜",
        "businesses": {
            "Farm Equipment Rental": {
                "inputs": [("equipment", "Equipment already available", "select", {"options": ["No", "Some", "Yes"]}), ("storage", "Equipment storage", "select", {"options": ["No", "Partial", "Yes"]}), ("capital", "Available investment (₹)", "number", {"min_value": 0, "value": 500000, "step": 10000}), ("operator", "Operator/technical labour", "number", {"min_value": 0, "value": 1, "step": 1}), ("fuel", "Fuel access", "select", {"options": ["Poor", "Moderate", "Good"]}), ("service_area", "Service area", "select", {"options": ["Village", "Multiple villages", "Taluk-wide"]}), ("farmer_demand", "Local farmer demand", "select", {"options": ["Low", "Medium", "High"]}), ("market_access", "Business/booking access", "select", {"options": ["Poor", "Moderate", "Good"]})],
                "requirements": {"Equipment": "Usable machinery/tools", "Storage": "Secure storage", "Operator": "Qualified operator where required", "Demand": "Sufficient local demand"},
                "weights": {"equipment": 20, "storage": 10, "capital": 15, "operator": 10, "fuel": 8, "service_area": 10, "farmer_demand": 17, "market_access": 10},
                "risks": ["Equipment downtime", "Fuel costs", "Low seasonal utilisation", "Maintenance costs"],
            },
            "Custom Farm Services": {
                "inputs": [("tools", "Tools/machinery available", "select", {"options": ["No", "Some", "Yes"]}), ("technical_skill", "Technical skill", "select", {"options": ["Beginner", "Intermediate", "Experienced"]}), ("operator", "Available operators", "number", {"min_value": 0, "value": 1, "step": 1}), ("fuel", "Fuel access", "select", {"options": ["Poor", "Moderate", "Good"]}), ("investment", "Available investment (₹)", "number", {"min_value": 0, "value": 300000, "step": 10000}), ("farmer_demand", "Local farmer demand", "select", {"options": ["Low", "Medium", "High"]}), ("service_area", "Service area", "select", {"options": ["Village", "Multiple villages", "Taluk-wide"]})],
                "requirements": {"Tools": "Relevant farm tools/equipment", "Skill": "Technical skill", "Demand": "Farmer demand", "Operations": "Operator availability"},
                "weights": {"tools": 18, "technical_skill": 16, "operator": 10, "fuel": 10, "investment": 14, "farmer_demand": 20, "service_area": 12},
                "risks": ["Seasonality", "Equipment breakdown", "Travel/fuel costs", "Demand uncertainty"],
            },
            "Agricultural Transport": {
                "inputs": [("vehicle", "Suitable vehicle available", "select", {"options": ["No", "Leased", "Yes"]}), ("vehicle_type", "Vehicle type", "select", {"options": ["Two-wheeler", "Auto/three-wheeler", "Pickup", "Mini truck", "Other"]}), ("storage", "Load/storage protection", "select", {"options": ["No", "Partial", "Yes"]}), ("driver", "Driver availability", "select", {"options": ["No", "Part-time", "Yes"]}), ("fuel", "Fuel access", "select", {"options": ["Poor", "Moderate", "Good"]}), ("investment", "Available investment (₹)", "number", {"min_value": 0, "value": 400000, "step": 10000}), ("farmer_demand", "Local demand", "select", {"options": ["Low", "Medium", "High"]}), ("service_area", "Service area", "select", {"options": ["Village", "Multiple villages", "Taluk-wide"]})],
                "requirements": {"Vehicle": "Suitable transport vehicle", "Driver": "Driver availability", "Demand": "Repeat local demand", "Fuel": "Fuel access"},
                "weights": {"vehicle": 20, "vehicle_type": 8, "storage": 8, "driver": 12, "fuel": 10, "investment": 15, "farmer_demand": 17, "service_area": 10},
                "risks": ["Fuel prices", "Vehicle maintenance", "Seasonal demand", "Road/transport delays"],
            },
            "Agricultural Equipment Repair": {
                "inputs": [("workshop", "Workshop space", "select", {"options": ["No", "Partial", "Yes"]}), ("tools", "Repair tools", "select", {"options": ["Poor", "Moderate", "Good"]}), ("skill", "Technical skill", "select", {"options": ["Beginner", "Intermediate", "Experienced"]}), ("spares", "Spare-parts access", "select", {"options": ["Poor", "Moderate", "Good"]}), ("electricity", "Electricity", "select", {"options": ["No", "Limited", "Reliable"]}), ("investment", "Available investment (₹)", "number", {"min_value": 0, "value": 150000, "step": 5000}), ("farmer_demand", "Local demand", "select", {"options": ["Low", "Medium", "High"]}), ("market_access", "Market access", "select", {"options": ["Poor", "Moderate", "Good"]})],
                "requirements": {"Workshop": "Repair workspace", "Tools": "Suitable repair tools", "Skill": "Technical repair skill", "Spare parts": "Reliable parts source", "Demand": "Local equipment demand"},
                "weights": {"workshop": 12, "tools": 18, "skill": 20, "spares": 13, "electricity": 8, "investment": 12, "farmer_demand": 12, "market_access": 5},
                "risks": ["Incorrect repairs", "Spare-parts delays", "Seasonality", "Equipment diversity"],
            },
        }
    },
}


# Add shared agricultural environment inputs to every agriculture activity.
# These appear only when the Agriculture domain is selected.
ENV_FACTOR_WEIGHTS = {
    "N": 9, "P": 9, "K": 9, "pH": 9,
    "Temperature": 9, "Humidity": 7, "Rainfall": 8
}

AGRICULTURE_ENV_INPUTS = [
    ("nitrogen", "Nitrogen (N)", "number", {"min_value": 0.0, "value": 70.0, "step": 1.0}),
    ("phosphorus", "Phosphorus (P)", "number", {"min_value": 0.0, "value": 40.0, "step": 1.0}),
    ("potassium", "Potassium (K)", "number", {"min_value": 0.0, "value": 40.0, "step": 1.0}),
    ("temperature", "Temperature (°C)", "number", {"min_value": -10.0, "max_value": 60.0, "value": 25.0, "step": 0.5}),
    ("humidity", "Humidity (%)", "number", {"min_value": 0.0, "max_value": 100.0, "value": 70.0, "step": 1.0}),
    ("soil_ph", "Soil pH", "number", {"min_value": 3.0, "max_value": 10.0, "value": 6.5, "step": 0.1, "format": "%.1f"}),
    ("rainfall", "Rainfall (mm)", "number", {"min_value": 0.0, "value": 700.0, "step": 25.0}),
]

for _ag_name, _ag_cfg in BUSINESS_DOMAIN_CONFIG.get("Agriculture", {}).get("businesses", {}).items():
    _existing = {x[0] for x in _ag_cfg["inputs"]}
    _extras = [x for x in AGRICULTURE_ENV_INPUTS if x[0] not in _existing]
    # Keep core environment factors together after season/land/water/irrigation.
    _ag_cfg["inputs"][0:0] = []
    insert_at = 0
    for i, item in enumerate(_ag_cfg["inputs"]):
        if item[0] in {"water", "irrigation"}:
            insert_at = i + 1
    _ag_cfg["inputs"][insert_at:insert_at] = _extras
    for _item in _extras:
        _ag_cfg["weights"].setdefault(_item[0], ENV_FACTOR_WEIGHTS.get({"nitrogen":"N","phosphorus":"P","potassium":"K","soil_ph":"pH","temperature":"Temperature","humidity":"Humidity","rainfall":"Rainfall"}.get(_item[0],""), 5))

# Category-level agriculture businesses reuse the core crop input model, while
# their candidate-crop set is filtered by category below.
_core_crop_cfg = BUSINESS_DOMAIN_CONFIG.get("Agriculture", {}).get("businesses", {}).get("Crop Cultivation", {})
for _cat_name in ("Cereals", "Pulses", "Oilseeds", "Commercial Crops"):
    if _cat_name in BUSINESS_DOMAIN_CONFIG.get("Agriculture", {}).get("businesses", {}):
        _cat_cfg = BUSINESS_DOMAIN_CONFIG["Agriculture"]["businesses"][_cat_name]
        _cat_cfg["inputs"] = list(_core_crop_cfg.get("inputs", []))
        _cat_cfg["requirements"] = dict(_core_crop_cfg.get("requirements", {}))
        _cat_cfg["weights"] = dict(_core_crop_cfg.get("weights", {}))

# Add a few direct aliases for the existing prototype business profiles.
BUSINESS_PROFILE_ALIAS = {
    "Dairy Farming": "Dairy / Milk-Based Business",
    "Goat Farming": "Goat / Sheep Rearing",
    "Sheep Farming": "Goat / Sheep Rearing",
    "Poultry Farming": "Poultry Farming",
    "Vegetable Cultivation": "Vegetable Cultivation",
    "Small Food Processing Unit": "Small Food Processing Unit",
}

FIELD_LABELS = {
    "water": "Water availability", "labour": "Labour", "investment": "Investment", "market_access": "Market access",
    "experience": "Experience", "electricity": "Electricity", "shed": "Housing/shed", "feed": "Feed availability",
    "veterinary": "Veterinary access", "fodder": "Fodder availability", "grazing": "Grazing/feed availability",
}


# ------------------------------------------------------------
# AGRICULTURE ENVIRONMENT ENGINE USED INSIDE BUSINESS RECOMMENDATION
# ------------------------------------------------------------
NPK_FILE_CANDIDATES = [
    "Crop_recommendation.csv", "crop_recommendation.csv", "Crop Recommendation.csv",
    "crop recommendation.csv", "NPK_crop_recommendation.csv"
]

@st.cache_data(show_spinner=False)
def load_npk_reference():
    """Load the uploaded NPK crop dataset when present in the app folder."""
    if pd is None:
        return None, "pandas is not installed"
    candidates = []
    for base in [Path.cwd(), Path(__file__).resolve().parent]:
        for name in NPK_FILE_CANDIDATES:
            f = base / name
            if f.exists():
                candidates.append(f)
    if not candidates:
        # Scan the app directory for compatible CSVs without requiring an exact filename.
        for f in Path.cwd().glob("*.csv"):
            try:
                cols = {str(c).strip().lower() for c in pd.read_csv(f, nrows=2).columns}
                if {"n", "p", "k", "temperature", "humidity", "ph", "rainfall", "label"}.issubset(cols):
                    candidates.append(f)
                    break
            except Exception:
                continue
    if not candidates:
        return None, "NPK reference CSV not found"
    try:
        df = pd.read_csv(candidates[0])
        rename = {c: str(c).strip().lower() for c in df.columns}
        df = df.rename(columns=rename)
        needed = ["n", "p", "k", "temperature", "humidity", "ph", "rainfall", "label"]
        if not set(needed).issubset(df.columns):
            return None, "NPK CSV does not contain the expected columns"
        for c in needed[:-1]:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        df["label"] = df["label"].astype(str).str.strip()
        df = df.dropna(subset=needed[:-1] + ["label"])
        return df, str(candidates[0])
    except Exception as exc:
        return None, f"Could not load NPK reference: {type(exc).__name__}"

CROP_CANONICAL_ALIASES = {
    "rice": "rice", "paddy": "rice", "maize": "maize", "corn": "maize",
    "cotton": "cotton", "chickpea": "chickpea", "bengal gram": "chickpea",
    "bengalgram": "chickpea", "pigeonpeas": "pigeonpeas", "pigeon pea": "pigeonpeas",
    "tur": "pigeonpeas", "groundnut": "groundnut", "peanut": "groundnut",
    "mungbean": "mungbean", "green gram": "mungbean", "blackgram": "blackgram",
    "black gram": "blackgram", "lentil": "lentil", "sorghum": "sorghum", "jowar": "sorghum",
    "wheat": "wheat", "sugarcane": "sugarcane", "banana": "banana", "mango": "mango",
    "papaya": "papaya", "pomegranate": "pomegranate", "chilli": "chilli", "chili": "chilli",
    "onion": "onion", "potato": "potato", "tomato": "tomato", "cucumber": "cucumber",
}

def _canonical_crop(name):
    k = str(name).strip().lower()
    return CROP_CANONICAL_ALIASES.get(k, k)

def _factor_match_score(value, series, full_points, critical=True):
    """Rule/statistical score using p10-p90 as the strong-fit band and p05-p95 as validity band."""
    if series is None or len(series) < 5:
        return None, True, "Reference range unavailable"
    p05, p10, p90, p95 = [float(series.quantile(q)) for q in (0.05, 0.10, 0.90, 0.95)]
    x = float(value)
    if x < p05 or x > p95:
        return 0.0, (False if critical else True), f"Outside reference validity band ({p05:.1f}–{p95:.1f})"
    if p10 <= x <= p90:
        return float(full_points), True, f"Inside strong-fit band ({p10:.1f}–{p90:.1f})"
    if x < p10:
        frac = (x - p05) / max(p10 - p05, 1e-9)
    else:
        frac = (p95 - x) / max(p95 - p90, 1e-9)
    return round(full_points * (0.5 + 0.5 * max(0.0, min(1.0, frac))), 2), True, f"Near edge of reference band ({p05:.1f}–{p95:.1f})"

def agriculture_environment_analysis(location, business_name, values):
    """Score location candidate crops against user-provided environment values."""
    candidates = []
    for _, items in _agriculture_options_for_business(business_name, location):
        candidates.extend(items)
    candidates = [c for c in candidates if not str(c).startswith("No verified")]
    df, source = load_npk_reference()
    if not candidates:
        return [], source

    inputs = {
        "N": values.get("nitrogen"), "P": values.get("phosphorus"), "K": values.get("potassium"),
        "pH": values.get("soil_ph"), "Temperature": values.get("temperature"),
        "Humidity": values.get("humidity"), "Rainfall": values.get("rainfall")
    }
    results = []
    if df is None:
        for crop in candidates:
            results.append({"crop": crop, "valid": True, "score": None, "breakdown": {}, "reason": "Environmental reference dataset unavailable"})
        return results, source

    labels = df["label"].apply(_canonical_crop)
    for crop in candidates:
        canon = _canonical_crop(crop)
        sub = df[labels == canon]
        if sub.empty:
            results.append({"crop": crop, "valid": False, "score": None, "breakdown": {}, "reason": "No matching crop rows in the uploaded NPK dataset"})
            continue
        breakdown = {}
        total = 0.0
        valid = True
        reasons = []
        for factor, points in ENV_FACTOR_WEIGHTS.items():
            val = inputs.get(factor)
            if val is None or (isinstance(val, (int, float)) and not isinstance(val, bool) and float(val) == 0):
                breakdown[factor] = "Not entered"
                continue
            col = factor.lower() if factor != "Temperature" else "temperature"
            if factor == "pH": col = "ph"
            if factor not in {"N", "P", "K", "Temperature", "Humidity", "Rainfall", "pH"}:
                continue
            series = sub[col]
            pts, ok, msg = _factor_match_score(val, series, points, critical=True)
            breakdown[factor] = {"score": pts, "max": points, "status": msg}
            if pts is not None:
                total += pts
            if not ok:
                valid = False
                reasons.append(f"{factor}: {msg}")
        results.append({"crop": crop, "valid": valid, "score": round(total, 1), "breakdown": breakdown,
                        "reason": "; ".join(reasons) if reasons else "Within the uploaded environmental reference bands"})
    results.sort(key=lambda r: (r["valid"], r["score"] if r["score"] is not None else -1), reverse=True)
    return results, source


def _profile_for_business(business_name):
    existing_name = BUSINESS_PROFILE_ALIAS.get(business_name)
    if not existing_name:
        return None
    return next((b for b in BUSINESSES if b.get("name") == existing_name), None)


def _scale_value(v, levels):
    return levels.get(v, 0.0)


def evaluate_business_config(business_name, values):
    """Adaptive 0-100 rule score. Missing/unknown inputs are excluded and the
    remaining configured weights are renormalized, so partial profiles still work."""
    _, cfg = business_config_for(business_name)
    if not cfg:
        return 0, [], ["Business configuration not found."]

    level = {
        "Poor": 0.10, "Very Low": 0.10, "Low": 0.20, "Limited": 0.40,
        "Moderate": 0.55, "Medium": 0.55, "Partial": 0.55, "Shared": 0.50,
        "Available": 0.75, "Good": 1.00, "High": 1.00, "Reliable": 1.00,
        "Yes": 1.00, "Experienced": 1.00, "Some experience": 0.65,
        "Intermediate": 0.65, "Beginner": 0.40, "No": 0.00, "None": 0.00,
        "Not sure": None, "Unknown": None, "Not provided": None, "": None
    }

    available_weight = 0.0
    earned = 0.0
    reasons = []
    gaps = []
    used_fields = 0
    missing_fields = []

    for key, weight in cfg.get("weights", {}).items():
        v = values.get(key)
        ratio = None

        if v is None or (isinstance(v, str) and v.strip() in {"", "Not sure", "Unknown", "Not provided"}):
            missing_fields.append(tr_any(FIELD_LABELS.get(key, key.replace("_", " ").title())))
            continue

        # Business numeric fields use 0 as the empty/default state. Do not
        # award feasibility credit for a field that has not been entered.
        if isinstance(v, (int, float)) and not isinstance(v, bool) and float(v) == 0:
            missing_fields.append(tr_any(FIELD_LABELS.get(key, key.replace("_", " ").title())))
            continue

        if isinstance(v, (int, float)) and not isinstance(v, bool):
            if key in {"investment", "capital"}:
                ratio = min(1.0, max(0.0, v / 100000.0))
            elif key in {"land_acres", "mulberry_land", "pond_area"}:
                ratio = min(1.0, max(0.0, v / 1.0))
            elif key in {"labour", "operator"}:
                ratio = min(1.0, max(0.0, v / 2.0))
            elif key in {"animals", "birds", "boxes", "workers"}:
                ratio = 1.0 if v > 0 else 0.0
            elif key in {"nitrogen", "phosphorus", "potassium", "soil_ph", "temperature", "humidity", "rainfall"}:
                # Environmental suitability is handled separately by the crop engine.
                # For the general business score, presence of a numeric reading earns credit.
                ratio = 1.0
            else:
                ratio = 1.0 if v > 0 else 0.0
        elif isinstance(v, str):
            ratio = level.get(v, 0.50)

        if ratio is None:
            missing_fields.append(tr_any(FIELD_LABELS.get(key, key.replace("_", " ").title())))
            continue

        ratio = max(0.0, min(1.0, float(ratio)))
        available_weight += weight
        earned += weight * ratio
        used_fields += 1

        label = tr_any(FIELD_LABELS.get(key, key.replace("_", " ").title()))
        if ratio >= 0.75:
            reasons.append(f"{label}: currently supports feasibility.")
        elif ratio < 0.45:
            gaps.append(f"{label}: needs attention before starting.")

    if available_weight <= 0:
        return 0, ["No usable business inputs were provided."], ["Provide at least the core inputs for the selected business."]

    score = round((earned / available_weight) * 100)
    if missing_fields:
        gaps.append("Missing or unknown inputs not used in the score: " + ", ".join(missing_fields[:6]) + ("..." if len(missing_fields) > 6 else ""))
    reasons.append(f"Adaptive scoring used {used_fields} available factor(s) and renormalized the configured weights.")
    return max(0, min(100, score)), reasons, gaps


def business_config_for(name):
    for domain_name, domain in BUSINESS_DOMAIN_CONFIG.items():
        if name in domain["businesses"]:
            return domain_name, domain["businesses"][name]
    return None, None


def render_business_input(key, label, kind, options, widget_key):
    """Render an input with consistent microcopy, tooltip, and practical defaults."""
    help_map = {
        "nitrogen": "Use the latest soil-test N value; this helps compare crop requirements.",
        "phosphorus": "Use the latest soil-test P value.",
        "potassium": "Use the latest soil-test K value.",
        "soil_ph": "Use the latest soil-test pH; most crops have a preferred pH band.",
        "temperature": "Enter the expected temperature during the production period.",
        "humidity": "Enter typical relative humidity for the production area.",
        "rainfall": "Enter expected seasonal rainfall or the relevant production-period value.",
        "investment": "Enter only capital you can actually deploy for this business.",
        "capital": "Enter the capital available for the service/business setup.",
        "land_acres": "Enter usable area, not total owned land if part is unavailable.",
        "pond_area": "Enter usable pond/culture area in acres.",
        "market_access": "Rate the practical access you have to buyers after transport and handling.",
        "water": "Select the dependable water availability for the planned scale.",
        "irrigation": "Select the irrigation reliability you can maintain during the production cycle.",
        "labour": "Enter people who can reliably work on the activity when needed.",
        "income_time": "Choose the time window in which you need the activity to start generating income.",
        "experience": "Choose the experience level you can rely on for this activity.",
        "farmer_demand": "Estimate current local demand from farmers or service buyers.",
        "electricity": "Consider the reliability of the electricity connection at the operating site.",
        "veterinary": "Select access to dependable animal-health support.",
        "water_quality": "Use a recent water-quality test where available.",
        "soil_type": "Choose the dominant soil type in the proposed production area.",
        "season": "Choose the intended production season.",
    }
    placeholder_map = {
        "text": "Enter a practical value",
    }
    help_text = help_map.get(key, f"Provide the most realistic current value for {label.lower()}.")
    if kind == "number":
        options = dict(options or {})
        # Business-page numeric inputs intentionally start at zero.
        # Streamlit requires min/value/max/step to use compatible numeric
        # types. Some business fields use fractional steps (e.g. acres),
        # so keep the whole number_input configuration consistently float
        # when any original numeric option was a float.
        numeric_values = [
            options.get("min_value"),
            options.get("max_value"),
            options.get("value"),
            options.get("step"),
        ]
        use_float = any(isinstance(v, float) for v in numeric_values if v is not None)
        if use_float:
            if options.get("max_value") is not None:
                options["max_value"] = float(options["max_value"])
            if options.get("step") is not None:
                options["step"] = float(options["step"])
            options["min_value"] = 0.0
            options["value"] = 0.0
        else:
            if options.get("max_value") is not None:
                options["max_value"] = int(options["max_value"])
            if options.get("step") is not None:
                options["step"] = int(options["step"])
            options["min_value"] = 0
            options["value"] = 0
        return st.number_input(tr_any(label), key=widget_key, help=tr_any(help_text), **options)
    if kind == "select":
        return st.selectbox(tr_any(label), options["options"], key=widget_key, help=tr_any(help_text), format_func=tr_any)
    if kind == "text":
        return st.text_input(tr_any(label), key=widget_key, help=tr_any(help_text), placeholder=tr_any(placeholder_map["text"]))
    return st.text_input(tr_any(label), key=widget_key, help=tr_any(help_text), placeholder=tr_any(placeholder_map["text"]))


def _input_group(key):
    """Map business-specific inputs into three progressive-disclosure cards."""
    climate = {"season","temperature","humidity","rainfall","climate","location","species","animal_type","breed","fish_species","plant","flower","product","service_type","equipment","vehicle_type","business_type","species_product"}
    soil_water = {"nitrogen","phosphorus","potassium","soil_ph","soil_type","soil_test","water","irrigation","water_quality","water_source","water_depth","pond_area","culture_area","land_acres","mulberry_land","growing_medium","feed","fodder","grazing","storage","cold_storage","drying","protected","shed","shed_area"}
    financial = {"investment","capital","working_capital","market_access","income_time","time_to_income","income_goal","risk_preference","experience","labour","workers","operator","driver","electricity","transport","farmer_demand","service_area","capacity","workspace","machinery","packaging"}
    if key in climate:
        return "location_climate"
    if key in soil_water:
        return "soil_water"
    if key in financial:
        return "capital_financial"
    return "capital_financial"


def _md_table(headers, rows):
    """Render a compact styled Markdown-like HTML table for comparison grids."""
    def esc(v):
        return str(v).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("|","&#124;")
    html=['<div class="gs-table-wrap"><table class="gs-table"><thead><tr>']
    html += [f'<th>{esc(h)}</th>' for h in headers]
    html.append('</tr></thead><tbody>')
    for row in rows:
        html.append('<tr>' + ''.join(f'<td>{esc(cell)}</td>' for cell in row) + '</tr>')
    html.append('</tbody></table></div>')
    st.markdown(''.join(html), unsafe_allow_html=True)


def business_success_rate(score):
    """Backward-compatible helper; returns the feasibility score, not a probability."""
    return max(0, min(100, round(float(score))))



# ------------------------------------------------------------
# BUSINESS RECOMMENDATION OUTPUT
# ------------------------------------------------------------

BUSINESS_OPTION_LIBRARY = {
    "Vegetable Cultivation": [
        {"name": "Tomato", "space": "Open field / protected cultivation depending on scale", "climate": "Warm conditions; verify season and local suitability", "cycle": "Typically a few months; verify variety and season", "market": "Local mandi, retailers, hotels, direct consumers"},
        {"name": "Onion", "space": "Open field; requires suitable soil and drainage", "climate": "Cooler growth period with suitable moisture management", "cycle": "Season-dependent", "market": "Mandi, wholesalers, retailers, institutional buyers"},
        {"name": "Chilli", "space": "Open field; spacing depends on variety", "climate": "Warm climate with controlled moisture", "cycle": "Season- and variety-dependent", "market": "Mandi, traders, processors, retailers"},
    ],
    "Fruit Cultivation": [
        {"name": "Banana", "space": "Open field with reliable water and drainage", "climate": "Warm conditions; frost-free environment preferred", "cycle": "Typically around one year depending on cultivar", "market": "Wholesalers, retailers, institutional buyers"},
        {"name": "Papaya", "space": "Open field with drainage and irrigation", "climate": "Warm conditions", "cycle": "Generally faster than orchard crops; cultivar-dependent", "market": "Wholesalers, retailers, processors"},
        {"name": "Guava", "space": "Orchard space with irrigation", "climate": "Warm to subtropical conditions", "cycle": "Longer establishment period; perennial crop", "market": "Fruit traders, retailers, processors"},
    ],
    "Floriculture": [
        {"name": "Rose", "space": "Open field or protected structure depending on production model", "climate": "Variety- and production-system dependent", "cycle": "Repeated harvest after establishment", "market": "Flower markets, florists, decorators, events"},
        {"name": "Gerbera", "space": "Often grown under protected cultivation for commercial consistency", "climate": "Needs controlled growing conditions for commercial quality", "cycle": "Repeated flower harvest after establishment", "market": "Florists, decorators, events, wholesale flower markets"},
        {"name": "Marigold", "space": "Open field", "climate": "Warm conditions; season-dependent", "cycle": "Shorter seasonal cycle than perennial flowers", "market": "Temples, events, florists, wholesale markets"},
    ],
    "Poultry Farming": [
        {"name": "Broiler Poultry", "space": "Shed space sized to flock density and local standards", "climate": "Requires ventilation and temperature management", "cycle": "Short production cycle; verify target live weight and local system", "market": "Local traders, retailers, restaurants, institutional buyers"},
        {"name": "Layer Poultry", "space": "Layer housing with adequate feeding, water and ventilation", "climate": "Requires environmental control and biosecurity", "cycle": "Longer production cycle than broilers; egg production is recurring", "market": "Egg wholesalers, retailers, bakeries, institutions"},
        {"name": "Rural Poultry", "space": "Smaller housing/free-range space depending on system", "climate": "Adapted to local conditions; health management remains essential", "cycle": "Longer/variable cycle than commercial broilers", "market": "Local households, traders, premium/direct buyers"},
    ],
    "Dairy Farming": [
        {"name": "Dairy Cattle", "space": "Covered shed with clean resting, feeding and drainage area", "climate": "Needs heat-stress and water management", "cycle": "Recurring milk production after calving; herd replacement is long-term", "market": "Milk collection centres, local retailers, direct consumers"},
        {"name": "Dairy Buffalo", "space": "Shed plus adequate water/cooling arrangements", "climate": "Strong attention to heat and water management", "cycle": "Recurring milk production after calving", "market": "Milk collection, dairies, local consumers"},
    ],
    "Goat Farming": [
        {"name": "Meat Goat Unit", "space": "Dry, ventilated shelter with feeding and movement area", "climate": "Generally adaptable; disease and heat management matter", "cycle": "Multiple growth/reproduction cycles; scale determines sales timing", "market": "Livestock traders, local markets, direct buyers"},
        {"name": "Breeding Goat Unit", "space": "Shelter plus controlled breeding area", "climate": "Local adaptation and health management required", "cycle": "Longer breeding cycle than short-term fattening", "market": "Breeding-stock buyers and livestock markets"},
    ],
    "Sheep Farming": [
        {"name": "Sheep Meat Unit", "space": "Dry shelter plus grazing/feed area", "climate": "Breed and local conditions determine suitability", "cycle": "Growth and breeding cycle depends on flock system", "market": "Livestock traders, local markets, institutional buyers"},
        {"name": "Sheep Breeding Unit", "space": "Shelter and managed breeding area", "climate": "Local breed and weather compatibility should be verified", "cycle": "Breeding cycle is longer than simple fattening", "market": "Breeding-stock buyers, livestock markets"},
    ],
    "Fish Farming": [
        {"name": "Freshwater Fish Farming", "space": "Pond/tank area sized to stocking and water management capacity", "climate": "Species-specific; water temperature and quality must be monitored", "cycle": "Species and stocking model dependent", "market": "Local fish markets, wholesalers, restaurants, direct buyers"},
        {"name": "Composite Fish Culture", "space": "Pond with adequate water management", "climate": "Species combination must match local water conditions", "cycle": "Species and stocking schedule dependent", "market": "Local markets, wholesalers and institutional buyers"},
    ],
    "Plant Nursery": [
        {"name": "Fruit Sapling Nursery", "space": "Nursery beds/containers with irrigation and shade/protection", "climate": "Depends on species and nursery conditions", "cycle": "Saleable stage varies by plant species", "market": "Farmers, gardeners, landscapers, horticulture projects"},
        {"name": "Vegetable Seedling Nursery", "space": "Protected/managed nursery area", "climate": "Requires controlled moisture and nursery hygiene", "cycle": "Short-cycle seedling production", "market": "Vegetable farmers, local growers, FPOs"},
        {"name": "Ornamental Nursery", "space": "Nursery space with shade and irrigation", "climate": "Species-dependent", "cycle": "Varies by plant", "market": "Households, landscapers, institutions"},
    ],
    "Beekeeping": [
        {"name": "Honey Bee Apiary", "space": "Apiary location with safe hive placement and access to forage", "climate": "Depends on forage availability and seasonal conditions", "cycle": "Honey harvest is seasonal/management-dependent", "market": "Direct consumers, retailers, processors"},
        {"name": "Migratory Beekeeping", "space": "Apiary equipment plus transport/logistics capability", "climate": "Follows flowering seasons across locations", "cycle": "Multiple seasonal honey flows possible", "market": "Bulk buyers, processors, direct retail"},
    ],
    "Mushroom Cultivation": [
        {"name": "Oyster Mushroom", "space": "Clean growing room or controlled production area", "climate": "Needs variety-specific temperature and humidity control", "cycle": "Short production cycles under suitable conditions", "market": "Local retailers, restaurants, direct consumers"},
        {"name": "Button Mushroom", "space": "More controlled production environment", "climate": "Requires tighter environmental management", "cycle": "Short production cycles under controlled conditions", "market": "Retailers, restaurants, institutional buyers"},
    ],
    "Sericulture": [
        {"name": "Mulberry Sericulture", "space": "Mulberry acreage plus rearing house", "climate": "Requires suitable mulberry growth and silkworm rearing conditions", "cycle": "Crop and silkworm cycles are seasonal/management-dependent", "market": "Cocoon markets, reelers, silk value chain"},
    ],
}

# User-facing Species / Variety / Product choices for EVERY business activity.
BUSINESS_SELECTION_OPTIONS = {
    "Crop Cultivation": ["Maize", "Groundnut", "Cotton", "Ragi", "Tur", "Bengal Gram"],
    "Cereals": ["Rice", "Maize", "Ragi", "Jowar", "Bajra", "Wheat"],
    "Pulses": ["Tur", "Bengal Gram", "Green Gram", "Black Gram", "Cowpea"],
    "Oilseeds": ["Groundnut", "Sunflower", "Soybean", "Sesame", "Safflower"],
    "Commercial Crops": ["Cotton", "Sugarcane", "Tobacco", "Commercial Maize", "Other commercial crop"],
    "Vegetable Cultivation": ["Tomato", "Onion", "Chilli", "Potato", "Cabbage", "Cauliflower", "Lady Finger", "Beans", "Cucumber"],
    "Fruit Cultivation": ["Banana", "Papaya", "Guava", "Pomegranate", "Grapes", "Orange", "Mango"],
    "Spice Cultivation": ["Chilli", "Turmeric", "Ginger", "Coriander", "Black Pepper", "Fenugreek"],
    "Floriculture": ["Rose", "Gerbera", "Marigold", "Chrysanthemum", "Jasmine"],
    "Poultry Farming": ["Broiler", "Layer", "Rural Poultry", "Backyard Poultry"],
    "Dairy Farming": ["Dairy Cattle", "Dairy Buffalo", "Mixed Dairy Unit"],
    "Goat Farming": ["Meat Goat", "Breeding Goat", "Dual-purpose Goat"],
    "Sheep Farming": ["Sheep Meat", "Sheep Breeding", "Dual-purpose Sheep"],
    "Fish Farming": ["Rohu", "Catla", "Mrigal", "Tilapia", "Freshwater Prawn", "Composite Fish Culture"],
    "Plant Nursery": ["Fruit Saplings", "Vegetable Seedlings", "Ornamental Plants", "Medicinal Plants"],
    "Fruit Nursery": ["Mango Saplings", "Guava Saplings", "Citrus Saplings", "Banana Planting Material", "Pomegranate Saplings"],
    "Flower Nursery": ["Rose Plants", "Marigold Plants", "Gerbera Plants", "Jasmine Plants", "Chrysanthemum Plants"],
    "Beekeeping": ["Apis cerana", "Apis mellifera", "Honey Bee Apiary", "Migratory Beekeeping"],
    "Mushroom Cultivation": ["Oyster Mushroom", "Button Mushroom", "Milky Mushroom", "Other Edible Mushroom"],
    "Sericulture": ["Mulberry Sericulture", "Silkworm Rearing", "Cocoon Production"],
    "Grain Milling": ["Rice Milling", "Maize Milling", "Ragi Flour", "Wheat Flour", "Pulse Milling"],
    "Spice Processing": ["Chilli Powder", "Turmeric Powder", "Coriander Powder", "Ginger Powder", "Spice Blends"],
    "Oil Extraction": ["Groundnut Oil", "Sunflower Oil", "Sesame Oil", "Coconut Oil", "Soybean Oil"],
    "Pickle / Jam / Food Processing": ["Mango Pickle", "Chilli Pickle", "Lemon Pickle", "Mango Jam", "Guava Jam", "Tomato-based Product"],
    "Milk Processing": ["Curd", "Paneer", "Ghee", "Flavoured Milk", "Milk-based Sweets"],
    "Farm Equipment Rental": ["Tractor Rental", "Rotavator Rental", "Power Tiller Rental", "Harvester Rental", "Sprayer Rental"],
    "Custom Farm Services": ["Land Preparation", "Sowing", "Spraying", "Harvesting", "Post-harvest Services"],
    "Agricultural Transport": ["Pickup Transport", "Mini Truck", "Tractor Trolley", "Three-wheeler Cargo", "Cold/Protected Transport"],
    "Agricultural Equipment Repair": ["Tractor Repair", "Power Tiller Repair", "Pump Repair", "Sprayer Repair", "Farm Implement Repair"],
}


def _contextual_selection_score(option_name, detail, domain_name, location):
    """Transparent rule-based ranking using location, climate, temperature and water."""
    ctx = LOCATION_CONTEXT.get(location, {})
    rainfall = automatic_location_rainfall(location)
    inferred_climate = (
        "Humid" if rainfall >= 1200 else
        "Dry" if rainfall <= 650 else
        "Semi-arid" if rainfall <= 800 else
        "Moderate"
    )
    climate = str(ctx.get("climate", inferred_climate)).lower()
    water = str(ctx.get("water", automatic_location_water(location))).lower()
    try:
        temp, _temp_source = get_location_temperature(location)
    except Exception:
        temp = safe_float(ctx.get("temperature_c", 25))
    text = " ".join(str(detail.get(k, "")) for k in ("climate", "space", "water", "cycle", "market")).lower()
    score = 50
    reasons = []

    if any(w in climate for w in ("dry", "semi-arid")):
        if any(w in text for w in ("dry", "semi-arid", "low water", "low–medium", "low-medium", "well-drained")):
            score += 18; reasons.append("dry/semi-arid compatibility")
        if "high rainfall" in text or "high water" in text:
            score -= 8
    elif "humid" in climate:
        if any(w in text for w in ("humid", "high rainfall", "water", "moisture", "pond", "fish")):
            score += 18; reasons.append("humid/moisture compatibility")
    else:
        if any(w in text for w in ("moderate", "warm", "local conditions", "adapted", "well-drained")):
            score += 10; reasons.append("moderate-climate compatibility")

    if water in {"limited", "low"}:
        if any(w in text for w in ("low water", "low–medium", "low-medium", "dry", "rain-fed")):
            score += 12; reasons.append("lower water demand")
        if any(w in text for w in ("reliable water", "high water", "high", "irrigation")):
            score -= 6
    elif water == "high":
        if any(w in text for w in ("water", "irrigation", "pond", "fish", "banana", "coconut")):
            score += 10; reasons.append("good water availability")
    elif "medium" in text or "water" in text:
        score += 4

    if temp >= 27 and any(w in text for w in ("cooler", "cool", "cold", "temperate")):
        score -= 10
    if temp <= 20 and any(w in text for w in ("warm", "heat")):
        score -= 8

    if domain_name == "Agriculture":
        mapped = set(suitable_crops_for_location(location))
        if option_name in mapped:
            score += 25
            reasons.insert(0, "mapped for selected location")

    return max(0, min(100, round(score))), reasons


def contextual_selection_options(business_name, domain_name, location):
    """Return options sorted by selected location/climate context."""
    if domain_name == "Agriculture":
        raw = []
        for _, items in _agriculture_options_for_business(business_name, location):
            raw.extend([str(x) for x in items if not str(x).startswith("No verified")])
        # Agriculture uses the location-to-crop mapping as the primary source.
        # The configured list is used only when the location mapping has no
        # candidates, so the species selector is genuinely location-aware.
        if not raw:
            raw = [str(x) for x in BUSINESS_SELECTION_OPTIONS.get(business_name, [])]
    else:
        raw = [str(x) for x in BUSINESS_SELECTION_OPTIONS.get(business_name, [])]

    raw = list(dict.fromkeys(raw))
    if not raw:
        return ["Not specified"]

    details = {str(d.get("name")): d for d in BUSINESS_OPTION_LIBRARY.get(business_name, [])
               if isinstance(d, dict) and d.get("name")}
    for opt in raw:
        details.setdefault(opt, {
            "name": opt,
            "space": "Use infrastructure appropriate to the selected activity and local scale.",
            "climate": "Use the selected location's climate profile; verify species/variety requirements locally.",
            "cycle": "Activity-specific; confirm the expected production/service cycle before investing.",
            "market": "Local buyers, retailers, institutions or direct customers depending on the activity.",
        })

    ranked = []
    for opt in raw:
        sc, reasons = _contextual_selection_score(opt, details[opt], domain_name, location)
        ranked.append((sc, opt, reasons))
    ranked.sort(key=lambda x: (-x[0], x[1]))
    return [x[1] for x in ranked]


def selection_detail_for(business_name, selected_option, domain_name, location):
    """Return a complete contextual answer for the selected species/variety/product."""
    detail = None
    for item in BUSINESS_OPTION_LIBRARY.get(business_name, []):
        if isinstance(item, dict) and str(item.get("name", "")) == str(selected_option):
            detail = dict(item)
            break

    if detail is None:
        profile = CROP_PROFILES.get(selected_option, {})
        detail = {
            "name": selected_option,
            "space": profile.get("soil", "Use infrastructure appropriate to the selected activity."),
            "climate": profile.get("climate", "Use the selected location's climate profile and verify locally."),
            "cycle": profile.get("duration", "Activity-specific; verify the expected cycle locally."),
            "market": "Local buyers, retailers, processors or direct customers depending on the activity.",
            "water": profile.get("water", "Activity-specific water requirement; verify locally."),
        }

    if domain_name == "Agriculture":
        profile = CROP_PROFILES.get(selected_option, {})
        if profile.get("water"):
            detail["water"] = profile["water"]
        if profile.get("duration"):
            detail["cycle"] = profile["duration"]
        if profile.get("soil"):
            detail["space"] = profile["soil"]

    sc, reasons = _contextual_selection_score(selected_option, detail, domain_name, location)
    detail["context_score"] = sc
    detail["reasons"] = reasons or ["configured for the selected activity"]
    detail["location"] = location
    detail["location_climate"] = LOCATION_CONTEXT.get(location, {}).get("climate", "Moderate")
    detail["location_temperature"] = LOCATION_CONTEXT.get(location, {}).get("temperature_c", 25)
    detail["location_water"] = LOCATION_CONTEXT.get(location, {}).get("water", "Medium")
    return detail



def _complete_business_option_library():
    """Fill detailed option records for every configured business activity.
    Existing curated records remain untouched; missing activities get useful,
    activity-specific guidance so every domain has selectable, explainable options.
    """
    templates = {
        "Crop Cultivation": ("Open field sized to the selected crop", "Use the selected location's climate and crop profile", "Crop-specific; use the profile and local season", "Mandi, traders, retailers, processors or direct buyers"),
        "Cereals": ("Open field with suitable soil and drainage", "Varies by cereal and local season", "Usually seasonal; crop-specific", "Mandi, millers, wholesalers and local buyers"),
        "Pulses": ("Open field with well-drained soil", "Generally suited to moderate/drier crop seasons; verify locally", "Short to medium crop cycle", "Mandi, dal mills, wholesalers and retailers"),
        "Oilseeds": ("Open field with well-drained soil", "Crop-specific; avoid unsuitable waterlogging", "Seasonal crop cycle", "Oil mills, traders, mandi and processors"),
        "Commercial Crops": ("Field or plantation space according to crop", "Crop-specific; match temperature and water needs", "Medium to long cycle depending on crop", "Processors, aggregators, mandi and contract/direct buyers"),
        "Spice Cultivation": ("Open field or protected plot depending on spice", "Warm conditions with crop-specific moisture management", "Short to long cycle depending on spice", "Spice traders, processors, retailers and mandi"),
        "Fruit Nursery": ("Nursery beds/containers with shade and irrigation", "Species-specific; protect young plants from extremes", "Months to saleable sapling stage", "Farmers, nurseries, landscapers and horticulture projects"),
        "Flower Nursery": ("Protected or open nursery space with irrigation", "Species-specific; controlled moisture improves establishment", "Weeks to months depending on plant", "Growers, florists, landscapers and local gardeners"),
        "Grain Milling": ("Clean milling room with power, storage and handling space", "Dry, ventilated processing environment; power reliability matters", "Continuous/batch processing", "Local retailers, wholesalers, institutions and packaged-food buyers"),
        "Spice Processing": ("Clean processing room with grinder, dryer and packing area", "Dry, hygienic processing conditions", "Batch-based processing", "Retailers, wholesalers, restaurants and packaged-food buyers"),
        "Oil Extraction": ("Food-grade processing room with expeller/press and storage", "Dry, clean and well-ventilated processing area", "Batch-based processing", "Retailers, local households, wholesalers and food businesses"),
        "Pickle / Jam / Food Processing": ("Clean food-processing and packaging workspace", "Hygienic, controlled processing and storage conditions", "Batch-based; product shelf life varies", "Local retailers, direct consumers, hotels and institutions"),
        "Milk Processing": ("Clean dairy-processing area with cold storage", "Temperature and hygiene control are essential", "Batch-based processing", "Local retailers, households, hotels and institutions"),
        "Farm Equipment Rental": ("Equipment parking, maintenance and dispatch space", "Adapt to local field seasons and road conditions", "Seasonal demand peaks; booking-based service", "Nearby farmers, FPOs and custom-hiring customers"),
        "Custom Farm Services": ("Equipment/service base with safe operating access", "Adapt service timing to local crop seasons and weather", "Job-based; seasonal peaks", "Nearby farmers, FPOs and farmer groups"),
        "Agricultural Transport": ("Vehicle parking and loading access", "Match vehicle type to local roads, weather and cargo", "Trip/job-based", "Farmers, traders, FPOs, mandis and processors"),
        "Agricultural Equipment Repair": ("Covered workshop with tools, spares and safe work area", "Dry workshop; protect tools and electrical equipment", "Job-based repair cycle", "Farmers, equipment owners, rental operators and FPOs"),
    }
    for business, opts in BUSINESS_SELECTION_OPTIONS.items():
        if business in BUSINESS_OPTION_LIBRARY:
            continue
        base = templates.get(business, (
            "Activity-appropriate workspace and basic infrastructure",
            "Use the selected location's climate profile and verify local requirements",
            "Activity-specific",
            "Local buyers, users or service customers",
        ))
        BUSINESS_OPTION_LIBRARY[business] = [
            {"name": opt, "space": base[0], "climate": base[1], "cycle": base[2], "market": base[3]}
            for opt in opts
        ]

_complete_business_option_library()

def business_selection_options(business_name, domain_name, location):
    """Return activity-specific options ranked automatically for the selected context."""
    return contextual_selection_options(business_name, domain_name, location)

BUSINESS_ADVICE = {
    "Poultry Farming": {
        "advice": [
            "Secure chicks, feed and veterinary support before stocking the first batch.",
            "Use a written feed, vaccination, mortality and cleaning schedule.",
            "Pre-arrange at least one reliable buyer and transport route before the sale window.",
        ],
        "steps": [
            "Complete shed preparation, ventilation, water, sanitation and biosecurity checks.",
            "Confirm chick supplier, feed supplier and health-support contact.",
            "Start the pilot batch at the selected scale and record daily feed use, mortality and growth.",
            "Lock the buyer/market route before the birds reach sale weight.",
            "Compare actual cycle cost and sales with the plan before expanding.",
        ],
    },
    "Dairy Farming": {
        "advice": [
            "Do not scale the herd beyond dependable fodder, water, shed and labour capacity.",
            "Track feed cost and milk yield animal-by-animal.",
            "Secure a milk collection or direct-selling channel before adding animals.",
        ],
        "steps": [
            "Prepare shed, drainage, water, fodder storage and cleaning arrangements.",
            "Finalize animal sourcing, veterinary support and feeding plan.",
            "Set up milk collection, chilling/transport or direct-sale arrangements.",
            "Start with the planned herd size and record yield, feed and health costs.",
            "Review the first production period before adding more animals.",
        ],
    },
    "Goat Farming": {
        "advice": [
            "Match herd size to year-round feed and water availability.",
            "Use dry housing, routine vaccination/deworming and quick disease response.",
            "Plan sales around local livestock-market demand rather than only herd growth.",
        ],
        "steps": [
            "Prepare secure shelter, fencing, feeding and water arrangements.",
            "Source healthy stock from a reliable supplier and arrange veterinary support.",
            "Set a feeding and health-monitoring schedule.",
            "Identify buyers and transport before the target sale period.",
            "Review mortality, feed cost and realized sale price before scaling.",
        ],
    },
    "Sheep Farming": {
        "advice": [
            "Plan flock size around grazing/feed availability and seasonal shortages.",
            "Maintain dry housing and preventive health management.",
            "Use market-linked sale planning instead of holding animals without a cost limit.",
        ],
        "steps": [
            "Prepare shelter, fencing, water and feed/grazing arrangements.",
            "Source healthy animals and arrange veterinary support.",
            "Set a vaccination, parasite-control and record-keeping routine.",
            "Confirm market and transport arrangements before sale.",
            "Review actual cost per animal and realized price before expansion.",
        ],
    },
    "Fish Farming": {
        "advice": [
            "Do not stock fish until pond condition and water quality are verified.",
            "Select species based on water conditions and the local selling channel.",
            "Monitor feed use, water quality, mortality and growth throughout the cycle.",
        ],
        "steps": [
            "Test and prepare the pond/water system before stocking.",
            "Confirm species, stocking plan and dependable seed/feed suppliers.",
            "Start the production cycle with a documented feeding and water-quality schedule.",
            "Secure buyers and harvesting/transport arrangements ahead of harvest.",
            "Review production cost, survival and realized sale price before increasing stocking density.",
        ],
    },
    "Plant Nursery": {
        "advice": [
            "Produce varieties with verified local demand instead of maximizing variety.",
            "Prioritize planting-material quality, irrigation and nursery hygiene.",
            "Track survival rate and sales by plant type before expanding.",
        ],
        "steps": [
            "Prepare nursery beds/containers, shade/protection and irrigation.",
            "Source reliable planting material and production inputs.",
            "Plan production batches around local planting seasons and customer demand.",
            "Build farmer, landscaper and retail buyer channels.",
            "Scale only after observing actual survival and sales data.",
        ],
    },
    "Beekeeping": {
        "advice": [
            "Verify forage/flower availability before placing colonies.",
            "Plan colony-health monitoring and pest management from day one.",
            "Use direct sales and quality packaging where local demand supports it.",
        ],
        "steps": [
            "Select a suitable apiary location and prepare hives/equipment.",
            "Source healthy colonies and establish forage/season management.",
            "Maintain routine inspection, pest and colony-health records.",
            "Prepare extraction, packaging and buyer arrangements.",
            "Review honey yield per colony and sales realization before adding colonies.",
        ],
    },
    "Mushroom Cultivation": {
        "advice": [
            "Treat contamination control and environmental stability as core production priorities.",
            "Secure reliable spawn and substrate before starting a batch.",
            "Pre-arrange fast local sales because fresh mushrooms are perishable.",
        ],
        "steps": [
            "Prepare a clean growing room and verify temperature/humidity control.",
            "Secure spawn, substrate and packaging supplies.",
            "Run a small pilot batch and record contamination and yield.",
            "Build retail, restaurant or direct-consumer sales before increasing batches.",
            "Scale only after the first batches show repeatable production and sales.",
        ],
    },
    "Sericulture": {
        "advice": [
            "Keep mulberry leaf availability ahead of planned silkworm capacity.",
            "Control rearing hygiene and monitor disease early.",
            "Align cocoon production with the local market/collection schedule.",
        ],
        "steps": [
            "Prepare mulberry area, irrigation and rearing space.",
            "Arrange healthy silkworm seed and technical support.",
            "Maintain feeding, hygiene and disease-monitoring schedules.",
            "Confirm cocoon collection/market arrangements.",
            "Review leaf use, labour, cocoon output and sale realization before scaling.",
        ],
    },
}

DEFAULT_ADVICE = [
    "Verify the main technical requirement and market channel before committing the full investment.",
    "Use current local quotations for the startup and working-capital plan.",
    "Start with a manageable pilot and scale only after recording actual operating results.",
]

DEFAULT_STEPS = [
    "Verify site/infrastructure and compliance requirements.",
    "Secure reliable input/resource suppliers.",
    "Run a small pilot and record actual operating performance.",
    "Secure a market channel before the sale/harvest/service window.",
    "Review actual costs, sales and operational problems before scaling.",
]


SCHEME_DETAILS = {
    "National Livestock Mission (NLM-EDP)": {
        "what_it_is": "Entrepreneurship support under the National Livestock Mission for specified rural poultry and small-ruminant activities, including entrepreneurship development in rural poultry and sheep/goat sectors.",
        "benefit": "Eligible projects can receive scheme-based capital subsidy/incentive support subject to the current component guidelines and approval process.",
        "eligibility": "Current guidelines specify eligible entities and project conditions; examples include individuals, SHGs, FPOs/FCOs, JLGs and Section 8 companies, with conditions such as trained entrepreneurship/expert support and land/loan or guarantee requirements for relevant components.",
        "use": "Relevant for eligible poultry or sheep/goat entrepreneurship, breed-development units and specified feed/fodder activities.",
        "note": "Eligibility, subsidy amount, project size and application route depend on the exact NLM component selected.",
        "source": "Department of Animal Husbandry & Dairying (DAHD) — National Livestock Mission / NLM-EDP"
    },
    "Animal Husbandry Infrastructure Development Fund (AHIDF)": {
        "what_it_is": "A financing support scheme for eligible animal-husbandry infrastructure and value-addition investments.",
        "benefit": "Current DAHD information covers dairy processing/value addition, meat processing, animal feed, breed improvement/multiplication, veterinary vaccine/drug manufacturing and animal-waste-to-wealth infrastructure; financing support is subject to scheme terms.",
        "eligibility": "Eligible individuals, private companies, MSMEs, FPOs, Section 8 companies and dairy cooperatives may qualify for specified activities under the current operational guidelines.",
        "use": "Most relevant when the business involves eligible dairy processing, feed, breeding, processing or other qualifying infrastructure rather than ordinary small livestock rearing alone.",
        "note": "Do not treat AHIDF as an automatic subsidy for every dairy or livestock unit; the exact infrastructure/activity must fall within the current eligible categories.",
        "source": "Department of Animal Husbandry & Dairying (DAHD) — AHIDF"
    },
    "Fisheries and Aquaculture Infrastructure Development Fund (FIDF)": {
        "what_it_is": "A concessional-finance framework for eligible fisheries and aquaculture infrastructure projects.",
        "benefit": "Financing support is available for eligible fisheries/aquaculture infrastructure through designated channels, subject to current scheme conditions.",
        "eligibility": "Eligibility depends on the beneficiary/project category and the infrastructure activity covered by the current FIDF guidelines.",
        "use": "Relevant for eligible aquaculture/fisheries infrastructure rather than treating it as a universal operating subsidy.",
        "note": "Check current FIDF validity, eligible activities and lending route before preparing a project.",
        "source": "Department of Fisheries, Government of India — FIDF"
    },
    "Mission for Integrated Development of Horticulture (MIDH)": {
        "what_it_is": "A horticulture development scheme supporting eligible horticulture activities through centrally supported/state implementation mechanisms.",
        "benefit": "Support varies by component and can cover specified horticulture development, planting material, protected cultivation, post-harvest or related infrastructure depending on the applicable component.",
        "eligibility": "Component-specific norms, cost ceilings, beneficiary conditions and implementation arrangements apply.",
        "use": "Relevant to eligible horticulture activities such as fruits, vegetables, flowers, nurseries and protected cultivation where the chosen component is covered.",
        "note": "Exact assistance must be checked against the current component and state/UT implementation guidelines.",
        "source": "Mission for Integrated Development of Horticulture (MIDH) / horticulture implementation guidelines"
    },
    "National Horticulture Board (NHB) Schemes": {
        "what_it_is": "NHB schemes support eligible commercial horticulture and related infrastructure/projects under current operational guidelines.",
        "benefit": "Assistance depends on the specific NHB scheme/component, project type, cost norms and admissibility conditions.",
        "eligibility": "Project-specific technical, financial and implementation requirements apply.",
        "use": "Relevant for eligible commercial horticulture, protected cultivation and related infrastructure where an NHB component applies.",
        "note": "Do not show an NHB benefit as guaranteed; the project must satisfy the current NHB guidelines and approval process.",
        "source": "National Horticulture Board (NHB)"
    },
    "Agriculture Infrastructure Fund (AIF)": {
        "what_it_is": "A financing facility for eligible post-harvest management and agricultural infrastructure projects.",
        "benefit": "Official scheme material provides eligible borrowers with interest-support and credit-facilitation benefits subject to scheme conditions.",
        "eligibility": "Eligibility depends on the borrower category and the infrastructure asset/project being financed.",
        "use": "More relevant to storage, grading, aggregation, primary processing and other eligible agricultural infrastructure than routine cultivation expenses.",
        "note": "The recommended project must fit an eligible infrastructure category and the current lending guidelines.",
        "source": "Government of India — Agriculture Infrastructure Fund"
    },
    "Kisan Credit Card (KCC)": {
        "what_it_is": "A formal agricultural credit mechanism for eligible crop and allied working-capital requirements.",
        "benefit": "Provides access to institutional credit for eligible agricultural/allied needs, subject to lender and eligibility conditions.",
        "eligibility": "Farmer/borrower eligibility and sanctioned limits depend on the participating financial institution and applicable KCC rules.",
        "use": "Relevant for working-capital needs in eligible crop and allied agricultural activities.",
        "note": "KCC is credit, not a direct capital subsidy; repayment and lending conditions apply.",
        "source": "Government of India / participating financial institutions"
    },
    "Pradhan Mantri MUDRA Yojana (PMMY)": {
        "what_it_is": "Institutional micro-credit support for eligible micro-enterprises through participating lenders.",
        "benefit": "Can support eligible micro-business financing needs subject to lender assessment and current PMMY categories/conditions.",
        "eligibility": "Eligibility and sanctioned amount depend on the business, applicant and participating lender.",
        "use": "Potentially relevant to small non-farm and eligible service/trading/manufacturing micro-enterprises, including some rural businesses.",
        "note": "The scheme does not guarantee approval; the lender assesses the application.",
        "source": "Department of Financial Services / participating lenders"
    },
    "PMEGP – Prime Minister's Employment Generation Programme": {
        "what_it_is": "A credit-linked programme supporting eligible new micro-enterprises through bank finance and margin-money subsidy.",
        "benefit": "Eligible projects may receive margin-money subsidy subject to current PMEGP guidelines, category and project conditions.",
        "eligibility": "Applicant, activity, project-cost and other eligibility requirements under the current PMEGP guidelines apply.",
        "use": "Relevant for eligible new micro-enterprise activities, particularly non-farm manufacturing and service enterprises and other covered activities.",
        "note": "The selected business must be an eligible PMEGP activity; subsidy is not automatic.",
        "source": "KVIC / Ministry of MSME — PMEGP"
    },
    "Agri-Clinics and Agri-Business Centres (ACABC)": {
        "what_it_is": "Support framework for eligible trained agriculture professionals establishing agri-clinics and agri-business centres.",
        "benefit": "Provides eligible project support according to current ACABC training, finance and subsidy provisions.",
        "eligibility": "Training/qualification, project, financing and other current ACABC conditions apply.",
        "use": "Relevant to agriculture advisory, farm services, input/services and eligible agri-business models.",
        "note": "Not intended as a general subsidy for every farm business.",
        "source": "MANAGE / Ministry of Agriculture & Farmers Welfare — ACABC"
    },
    "National Beekeeping and Honey Mission (NBHM)": {
        "what_it_is": "A national support programme for scientific beekeeping, honey and related value-chain development under the applicable programme guidelines.",
        "benefit": "Support depends on the approved activity/component and implementing agency; assistance can be linked to beekeeping development, equipment, training or value-chain activities where permitted.",
        "eligibility": "Beneficiary and activity conditions vary by component and implementing agency.",
        "use": "Relevant to eligible beekeeping and honey-value-chain activities.",
        "note": "Check the current implementing-agency guidelines before treating a component as available to an individual applicant.",
        "source": "Government of India — National Beekeeping and Honey Mission"
    },
    "PMFME – Pradhan Mantri Formalisation of Micro Food Processing Enterprises": {
        "what_it_is": "A food-processing enterprise support scheme covering eligible micro food-processing units and group/common-infrastructure models.",
        "benefit": "For eligible individual micro food-processing units, the official PMFME portal states credit-linked capital subsidy of 35% of eligible project cost, up to ₹10 lakh per unit; group/common infrastructure has separate limits and conditions.",
        "eligibility": "Eligibility, beneficiary contribution, bank finance, ODOP alignment and other current PMFME conditions apply.",
        "use": "Directly relevant to eligible micro food-processing activities such as spice processing, milling, pickles and other value-added food products.",
        "note": "The subsidy is credit-linked and subject to the current PMFME guidelines and approval process.",
        "source": "Ministry of Food Processing Industries (MoFPI) — PMFME"
    },
}

SCHEME_ALIASES = {
    "AHIDF": "Animal Husbandry Infrastructure Development Fund (AHIDF)",
    "FIDF": "Fisheries and Aquaculture Infrastructure Development Fund (FIDF)",
}

def related_scheme_names(business_name, profile=None):
    names = BUSINESS_SCHEME_MAP.get(business_name, [])
    if not names and profile:
        names = profile.get("schemes", [])
    normalized = [SCHEME_ALIASES.get(n, n) for n in names]
    # Resolve common naming variants to the actual keys available in SCHEME_DETAILS.
    detail_keys = set(SCHEME_DETAILS.keys())
    aliases = {
        "National Livestock Mission (NLM-EDP)": "National Livestock Mission (NLM)",
        "Kisan Credit Card": "Kisan Credit Card (KCC)",
        "PM MUDRA Yojana (PMMY)": "Pradhan Mantri MUDRA Yojana (PMMY)",
    }
    normalized = [aliases.get(n, n) for n in normalized]
    return [n for n in dict.fromkeys(normalized) if n in detail_keys]

def _location_category_crops(location):
    """Return all crops configured for the selected location, grouped by category."""
    crops = suitable_crops_for_location(location)
    grouped = {}
    for crop in crops:
        category = crop_category(crop)
        grouped.setdefault(category, []).append(crop)
    order = ["Vegetable", "Leafy", "Fruit", "Horticulture", "Cereal", "Pulse", "Oilseed", "Spice", "Commercial", "Other"]
    return {k: grouped[k] for k in order if k in grouped}

def _agriculture_options_for_business(name, location):
    grouped = _location_category_crops(location)
    if name == "Vegetable Cultivation":
        return [("Vegetables", grouped.get("Vegetable", []) + grouped.get("Leafy", []))]
    if name == "Fruit Cultivation":
        return [("Fruits", grouped.get("Fruit", []) + grouped.get("Horticulture", []))]
    if name == "Cereals":
        return [("Cereals", grouped.get("Cereal", []))]
    if name == "Pulses":
        return [("Pulses", grouped.get("Pulse", []))]
    if name == "Oilseeds":
        return [("Oilseeds", grouped.get("Oilseed", []))]
    if name == "Spice Cultivation":
        return [("Spices", grouped.get("Spice", []))]
    if name == "Commercial Crops":
        return [("Commercial Crops", grouped.get("Commercial", []))]
    if name == "Floriculture":
        return [("Flowers", [])]
    if name in {"Crop Cultivation", "Plant Nursery"}:
        return [(k, v) for k, v in grouped.items()]
    return []

def _option_candidates(name, domain_name, location):
    if domain_name == "Agriculture":
        grouped = _agriculture_options_for_business(name, location)
        if any(items for _, items in grouped):
            return grouped
        if name == "Floriculture":
            return [("Flowers", ["No verified location-to-flower mapping is present in the current dataset."])]
    opts = BUSINESS_OPTION_LIBRARY.get(name, [])
    if opts:
        return [("Business options", opts[:3])]
    return []

def dynamic_risk_analysis(name, cfg, values, score, location):
    """Generate risks from the selected business AND the user's actual inputs.
    This is a rule-based decision-support layer, not a statistical probability model.
    """
    risks = []

    def add(title, level, trigger, mitigation):
        impact_map = {
            "High": "High potential impact on output, cost, continuity or safety",
            "Medium": "Moderate potential impact on output, cost, continuity or marketability",
            "Low": "Lower potential impact when routine controls are maintained",
        }
        risks.append({
            "title": title,
            "level": level,
            "trigger": trigger,
            "impact": impact_map.get(level, "Potential impact"),
            "mitigation": mitigation,
        })

    water = str(values.get("water", ""))
    irrigation = str(values.get("irrigation", ""))
    market = str(values.get("market_access", ""))
    vet = str(values.get("veterinary", ""))
    feed = str(values.get("feed", values.get("fodder", "")))
    electricity = str(values.get("electricity", ""))
    labour = safe_float(values.get("labour", 0))
    investment = safe_float(values.get("investment", 0))
    experience = str(values.get("experience", ""))
    transport = str(values.get("transport", ""))
    shed = str(values.get("shed", ""))
    storage = str(values.get("storage", ""))
    equipment = str(values.get("equipment", ""))
    soil_test = str(values.get("soil_test", ""))
    income_time = str(values.get("income_time", ""))

    # Universal commercial risks driven by actual conditions.
    if market == "Poor":
        add("Market-access risk", "High",
            "The selected market-access level is Poor.",
            "Identify at least two buyers before scaling, compare local prices weekly, and avoid expanding production until a selling channel is confirmed.")
    elif market == "Moderate":
        add("Market-access risk", "Medium",
            "The selected market-access level is Moderate.",
            "Maintain at least two buyer channels and compare prices before each sales cycle.")

    if investment <= 0:
        add("Capital risk", "High",
            "No available investment has been entered.",
            "Prepare a complete startup and working-capital budget before committing to the activity.")
    elif score < 60:
        add("Execution-capital risk", "High",
            f"Current feasibility score is {score}/100.",
            "Start with a smaller pilot, close the highest-impact resource gaps, and only then consider scaling.")

    if experience == "Beginner":
        add("Experience / execution risk", "Medium",
            "The selected experience level is Beginner.",
            "Use a small pilot, obtain practical training, and arrange mentoring or technical support before full-scale operation.")

    if labour == 0 and "labour" in cfg.get("weights", {}):
        add("Labour-availability risk", "High",
            "Available labour is zero while the business requires labour.",
            "Secure named workers or service support before launch and define peak-season labour requirements.")
    elif labour < 1 and "labour" in cfg.get("weights", {}):
        add("Labour-availability risk", "Medium",
            "Limited labour has been entered.",
            "Plan labour for the busiest operating period and arrange backup support.")

    if water in {"None", "Low"} and "water" in cfg.get("weights", {}):
        add("Water-availability risk", "High" if water == "None" else "Medium",
            f"Water availability is set to {water}.",
            "Secure a reliable source before scaling and maintain a contingency arrangement appropriate to the activity.")
    elif irrigation in {"Rain-fed", "Limited"} and "irrigation" in cfg.get("weights", {}):
        add("Irrigation reliability risk", "Medium",
            f"Irrigation is {irrigation}.",
            "Plan crop/activity cycles around available water and arrange backup irrigation where technically feasible.")

    # Livestock / animal-specific triggers.
    if any(x in name.lower() for x in ["poultry", "dairy", "goat", "sheep"]):
        if shed in {"No", "Partial"}:
            add("Housing risk", "High" if shed == "No" else "Medium",
                f"Housing availability is {shed}.",
                "Complete suitable housing, ventilation, drainage, sanitation and protection arrangements before increasing the animal population.")
        if vet in {"No", "Limited"}:
            add("Animal-health risk", "High" if vet == "No" else "Medium",
                f"Veterinary support access is {vet}.",
                "Arrange a reliable veterinary contact, vaccination/health schedule and a rapid-response plan before stocking animals.")
        if feed in {"Poor", "Moderate"}:
            add("Feed / fodder cost risk", "High" if feed == "Poor" else "Medium",
                f"Feed/fodder availability is {feed}.",
                "Lock in more than one supplier, track feed/fodder cost per animal or bird, and maintain a short contingency stock.")

    # Poultry-specific risk logic.
    if "poultry" in name.lower():
        birds = safe_float(values.get("birds", 0))
        if birds >= 1000 and vet != "Good":
            add("Scale-related biosecurity risk", "High",
                f"The planned bird count is {int(birds):,} while veterinary support is not Good.",
                "Use a written biosecurity protocol, controlled visitor access, routine sanitation and a documented vaccination/health plan before scaling.")
        if electricity in {"No", "Limited"}:
            add("Power / heat-stress risk", "Medium",
                f"Electricity reliability is {electricity}.",
                "Plan backup power and ventilation/temperature management suitable for the production system.")

    # Dairy-specific risk logic.
    if "dairy" in name.lower():
        if equipment in {"No", "Partial"}:
            add("Milk-handling risk", "Medium",
                f"Milking/chilling equipment availability is {equipment}.",
                "Define clean milking, cooling, storage and collection arrangements to protect milk quality.")

    # Aquaculture / fish-specific triggers.
    if "fish" in name.lower() or "aquaculture" in name.lower():
        water_quality = str(values.get("water_quality", ""))
        if water_quality in {"Poor", "Unknown", ""}:
            add("Water-quality risk", "High",
                "Water quality is missing, unknown or poor.",
                "Test the water before stocking and monitor the critical water parameters required for the selected species.")
        if feed in {"Poor", "Moderate"}:
            add("Feed and growth risk", "Medium",
                f"Feed availability is {feed}.",
                "Establish a dependable feed source and monitor feed conversion, mortality and growth before expanding.")

    # Processing / services / equipment risks.
    if "processing" in cfg.get("domain", "").lower() or any(k in name.lower() for k in ["milling", "processing", "repair", "equipment rental"]):
        if electricity in {"No", "Limited"}:
            add("Operational downtime risk", "Medium",
                f"Electricity availability is {electricity}.",
                "Plan backup power or an alternative operating arrangement and schedule preventive equipment maintenance.")
        if equipment in {"No", "Partial"}:
            add("Equipment-capacity risk", "Medium",
                f"Equipment availability is {equipment}.",
                "Confirm machine capacity, service support, spare parts and maintenance costs before purchasing or scaling.")

    # Post-harvest / perishability signals.
    if transport in {"No", "Shared"} and any(x in name.lower() for x in ["vegetable", "floriculture", "flower", "nursery", "milk", "food", "mushroom"]):
        add("Post-harvest / transport risk", "Medium",
            f"Transport availability is {transport} for a time-sensitive product.",
            "Pre-arrange transport and buyer collection windows so harvested/produced stock is not held longer than necessary.")

    if storage in {"No", "Partial"} and any(x in name.lower() for x in ["grain", "spice", "oil", "processing"]):
        add("Storage risk", "Medium",
            f"Storage availability is {storage}.",
            "Define safe storage capacity and quality-control procedures before purchasing large quantities of raw material.")

    if soil_test == "No" and any(x in name.lower() for x in ["crop", "vegetable", "fruit", "spice", "floriculture"]):
        add("Soil-information risk", "Medium",
            "A soil test is not available.",
            "Obtain a soil test before making crop-specific nutrient decisions and use results to refine the plan.")

    # Time-goal mismatch: don't call it a failure; flag it as a planning risk.
    if income_time == "Within 3 months" and any(x in name.lower() for x in ["fruit", "orchard", "sericulture"]):
        add("Time-to-income mismatch", "High",
            "The target is income within 3 months for an activity that may require a longer establishment cycle.",
            "Choose a suitable short-cycle component, revise the income timeline, or begin with an additional faster-cashflow activity where appropriate.")

    # Always include baseline business-specific risks that were not triggered, with lower prominence.
    configured = cfg.get("risks", [])
    triggered_titles = {r["title"] for r in risks}
    fallback_map = {
        "Disease and mortality": ("Biological health risk", "High", "A health event can reduce output, quality and continuity.", "Maintain hygiene, preventive health procedures, observation records and an early-response contact."),
        "Feed-cost changes": ("Input-cost risk", "Medium", "Feed/fodder price changes can increase unit production cost.", "Track feed cost per unit, compare suppliers and maintain a small contingency stock."),
        "Market-price changes": ("Price risk", "Medium", "Selling prices can change between production and sale.", "Compare at least two buyer channels, record realized prices and avoid committing all output to one buyer."),
        "Pest/disease pressure": ("Biological crop risk", "Medium", "Pests or diseases can reduce crop yield and quality.", "Scout regularly, use preventive integrated management and act early when symptoms are detected."),
        "Weather variability": ("Climate risk", "Medium", "Unexpected weather can affect production timing, quality or yield.", "Use season-appropriate planning, monitor forecasts and maintain a practical contingency response."),
        "Water-quality failure": ("Water-quality risk", "High", "Poor water quality can affect production performance and product safety.", "Test water before production and monitor the critical quality parameters required by the activity."),
        "Perishability": ("Perishability risk", "High", "Time-sensitive products can lose value quickly after harvest or production.", "Pre-arrange buyers and transport, use appropriate handling/storage and align production with realistic sales windows."),
        "Equipment downtime": ("Equipment downtime risk", "Medium", "Unexpected equipment failure can interrupt operations and delay service or production.", "Use preventive maintenance, keep critical spares available and arrange a repair/service contact."),
    }
    for base_risk in configured:
        title, level, impact, mitigation = fallback_map.get(
            base_risk,
            (base_risk, "Low", "The activity has a lower-level baseline exposure that still needs routine monitoring.",
             "Monitor this risk on a defined schedule and record corrective action before scaling.")
        )
        if title not in triggered_titles and len(risks) < 8:
            risks.append({"title": title, "level": level, "trigger": "Business-specific baseline risk.", "impact": impact, "mitigation": mitigation})
            triggered_titles.add(title)

    priority = {"High": 0, "Medium": 1, "Low": 2}
    risks.sort(key=lambda r: (priority.get(r["level"], 9), r["title"]))
    return risks[:8]


def render_dynamic_risk_analysis(name, risks):
    """Show three risk levels and actionable controls without repeating trigger text."""
    if not risks:
        st.info(tr_any("No risk rules were triggered for the current business profile. Continue routine monitoring before scaling."))
        return
    counts={"High":0,"Medium":0,"Low":0}
    for r in risks:
        lvl=r.get("level","Low")
        counts[lvl if lvl in counts else "Low"] += 1
    total=sum(counts.values()) or 1
    high_pct=round(counts["High"]/total*100); med_pct=round(counts["Medium"]/total*100); low_pct=100-high_pct-med_pct
    st.caption(tr_any("Risk distribution is recalculated from the selected business and the current inputs."))
    c1,c2,c3=st.columns(3)
    c1.markdown(f'<div class="gs-metric"><div class="label">High Risk</div><div class="value">🔴 {high_pct}%</div><div>{counts["High"]} item(s)</div></div>',unsafe_allow_html=True)
    c2.markdown(f'<div class="gs-metric"><div class="label">Medium Risk</div><div class="value">🟠 {med_pct}%</div><div>{counts["Medium"]} item(s)</div></div>',unsafe_allow_html=True)
    c3.markdown(f'<div class="gs-metric"><div class="label">Low Risk</div><div class="value">🟢 {low_pct}%</div><div>{counts["Low"]} item(s)</div></div>',unsafe_allow_html=True)
    grouped={"High":[],"Medium":[],"Low":[]}
    for r in risks: grouped.get(r.get("level","Low"),grouped["Low"]).append(r)
    for level,title,cls in [("High","🔴 HIGH RISK","gs-risk-high"),("Medium","🟠 MEDIUM RISK","gs-risk-medium"),("Low","🟢 LOW RISK","gs-risk-low")]:
        if not grouped[level]: continue
        st.markdown(f"#### {tr_any(title)}")
        for r in grouped[level]:
            st.markdown(
                f'<div class="gs-card {cls}"><b>{tr_any(r["title"])}</b>'
                f'<br><span class="small-note"><b>{tr_any("Impact")}:</b> {tr_any(r.get("impact","Potential impact"))}</span>'
                f'<br><span class="small-note"><b>{tr_any("Control / mitigation")}:</b> {tr_any(r.get("mitigation","Monitor and manage this risk before scaling."))}</span></div>',
                unsafe_allow_html=True
            )

def _irrigation_score(values):
    """Transparent irrigation/water feasibility score out of 10."""
    water = str(values.get("water", "None"))
    irrigation = str(values.get("irrigation", "Rain-fed"))
    water_pts = {"None": 0, "Low": 2, "Medium": 4, "High": 5}.get(water, 2)
    irr_pts = {"Rain-fed": 2, "Limited": 2.5, "Available": 4, "Reliable": 5}.get(irrigation, 2)
    # Keep total bounded at 10 and make the result explainable.
    return round(min(10.0, water_pts + irr_pts), 1)


def _agriculture_environment_summary(location, business_name, values):
    """Return environment + irrigation analysis for the agriculture branch."""
    env_results, env_source = agriculture_environment_analysis(location, business_name, values)
    irrigation = _irrigation_score(values)
    return env_results, env_source, irrigation


BUSINESS_SCHEME_MAP = {
    "Crop Cultivation": ["Kisan Credit Card (KCC)", "Agriculture Infrastructure Fund (AIF)", "Agri-Clinics and Agri-Business Centres (ACABC)"],
    "Cereals": ["Kisan Credit Card (KCC)", "Agriculture Infrastructure Fund (AIF)"],
    "Pulses": ["Kisan Credit Card (KCC)", "Agriculture Infrastructure Fund (AIF)"],
    "Oilseeds": ["Kisan Credit Card (KCC)", "Agriculture Infrastructure Fund (AIF)"],
    "Commercial Crops": ["Kisan Credit Card (KCC)", "Agriculture Infrastructure Fund (AIF)", "Agri-Clinics and Agri-Business Centres (ACABC)"],
    "Vegetable Cultivation": ["Mission for Integrated Development of Horticulture (MIDH)", "National Horticulture Board (NHB) Schemes", "Kisan Credit Card (KCC)"],
    "Fruit Cultivation": ["Mission for Integrated Development of Horticulture (MIDH)", "National Horticulture Board (NHB) Schemes", "Kisan Credit Card (KCC)"],
    "Spice Cultivation": ["Mission for Integrated Development of Horticulture (MIDH)", "Kisan Credit Card (KCC)", "Agriculture Infrastructure Fund (AIF)"],
    "Floriculture": ["Mission for Integrated Development of Horticulture (MIDH)", "National Horticulture Board (NHB) Schemes", "Kisan Credit Card (KCC)"],
    "Poultry Farming": ["National Livestock Mission (NLM-EDP)", "Animal Husbandry Infrastructure Development Fund (AHIDF)", "Kisan Credit Card (KCC)"],
    "Dairy Farming": ["Animal Husbandry Infrastructure Development Fund (AHIDF)", "National Livestock Mission (NLM-EDP)", "Kisan Credit Card (KCC)"],
    "Goat Farming": ["National Livestock Mission (NLM-EDP)", "Kisan Credit Card (KCC)"],
    "Sheep Farming": ["National Livestock Mission (NLM-EDP)", "Kisan Credit Card (KCC)"],
    "Fish Farming": ["Fisheries and Aquaculture Infrastructure Development Fund (FIDF)", "Kisan Credit Card (KCC)", "Agriculture Infrastructure Fund (AIF)"],
    "Plant Nursery": ["Mission for Integrated Development of Horticulture (MIDH)", "National Horticulture Board (NHB) Schemes"],
    "Fruit Nursery": ["Mission for Integrated Development of Horticulture (MIDH)", "National Horticulture Board (NHB) Schemes", "Kisan Credit Card (KCC)"],
    "Flower Nursery": ["Mission for Integrated Development of Horticulture (MIDH)", "National Horticulture Board (NHB) Schemes", "Kisan Credit Card (KCC)"],
    "Beekeeping": ["National Beekeeping and Honey Mission (NBHM)", "Kisan Credit Card (KCC)", "PMFME – Pradhan Mantri Formalisation of Micro Food Processing Enterprises"],
    "Mushroom Cultivation": ["Agriculture Infrastructure Fund (AIF)", "PMFME – Pradhan Mantri Formalisation of Micro Food Processing Enterprises", "Kisan Credit Card (KCC)"],
    "Sericulture": ["Kisan Credit Card (KCC)", "Agriculture Infrastructure Fund (AIF)"],
    "Grain Milling": ["PMFME – Pradhan Mantri Formalisation of Micro Food Processing Enterprises", "Agriculture Infrastructure Fund (AIF)", "PMEGP – Prime Minister's Employment Generation Programme"],
    "Spice Processing": ["PMFME – Pradhan Mantri Formalisation of Micro Food Processing Enterprises", "Agriculture Infrastructure Fund (AIF)", "PMEGP – Prime Minister's Employment Generation Programme"],
    "Oil Extraction": ["PMFME – Pradhan Mantri Formalisation of Micro Food Processing Enterprises", "Agriculture Infrastructure Fund (AIF)", "PMEGP – Prime Minister's Employment Generation Programme"],
    "Pickle / Jam / Food Processing": ["PMFME – Pradhan Mantri Formalisation of Micro Food Processing Enterprises", "PMEGP – Prime Minister's Employment Generation Programme", "Pradhan Mantri MUDRA Yojana (PMMY)"],
    "Milk Processing": ["PMFME – Pradhan Mantri Formalisation of Micro Food Processing Enterprises", "Animal Husbandry Infrastructure Development Fund (AHIDF)", "PMEGP – Prime Minister's Employment Generation Programme"],
    "Farm Equipment Rental": ["Agriculture Infrastructure Fund (AIF)", "Agri-Clinics and Agri-Business Centres (ACABC)", "Pradhan Mantri MUDRA Yojana (PMMY)"],
    "Custom Farm Services": ["Agri-Clinics and Agri-Business Centres (ACABC)", "Agriculture Infrastructure Fund (AIF)", "Pradhan Mantri MUDRA Yojana (PMMY)"],
    "Agricultural Transport": ["Pradhan Mantri MUDRA Yojana (PMMY)", "PMEGP – Prime Minister's Employment Generation Programme", "Kisan Credit Card (KCC)"],
    "Agricultural Equipment Repair": ["Pradhan Mantri MUDRA Yojana (PMMY)", "PMEGP – Prime Minister's Employment Generation Programme", "Agri-Clinics and Agri-Business Centres (ACABC)"],
}

def schemes_for_business(business_name):
    """Return only scheme names that have full metadata in SCHEME_DETAILS."""
    return related_scheme_names(business_name, None)


# ============================================================
# BUSINESS-SPECIFIC PRIORITY GAPS
# ============================================================
# These gaps are derived from the selected business configuration rather than
# from a generic list.  Each business has different weighted requirements, so
# the gaps shown in the dashboard change automatically when the user changes
# the business/activity.
BUSINESS_GAP_ACTIONS = {
    "market_access": "Confirm at least two realistic buyer channels for this business and compare prices before each sales cycle.",
    "water": "Confirm a dependable water source at the planned scale and keep a backup arrangement before starting.",
    "water_availability": "Confirm the quantity and reliability of water required by this business before scaling.",
    "irrigation": "Set up reliable irrigation or a practical water-supply schedule suited to the selected activity.",
    "land_acres": "Confirm the usable land area and keep the planned scale within the available area.",
    "pond_area": "Confirm the usable pond/culture area and verify that it can support the planned stocking level.",
    "investment": "Prepare the complete startup and working-capital budget and keep a contingency amount before launch.",
    "capital": "Prepare the complete capital and working-capital budget before purchasing equipment or inventory.",
    "labour": "Arrange dependable labour for the peak operating period and keep backup support available.",
    "experience": "Complete practical training or work with an experienced operator before moving beyond the pilot stage.",
    "soil_test": "Obtain a recent soil test and use the result to make business-specific crop and nutrient decisions.",
    "season": "Align the production schedule with the appropriate local season and avoid starting outside the suitable window.",
    "temperature": "Confirm that the planned activity or selected crop/variety is suited to the location's temperature range.",
    "humidity": "Plan humidity-sensitive disease, hygiene or storage controls appropriate to the selected activity.",
    "rainfall": "Compare expected rainfall with the activity's water requirement and prepare irrigation or drainage support.",
    "transport": "Arrange dependable transport and a realistic collection/delivery schedule before production or sales begin.",
    "storage": "Confirm suitable storage capacity and handling procedures to reduce spoilage, damage and quality loss.",
    "cold_storage": "Confirm cold-storage access or an alternative fast-selling/transport plan before handling perishables.",
    "shed": "Complete suitable housing/shed, ventilation, drainage and sanitation before stocking animals or birds.",
    "shed_area": "Confirm that the available shed area is sufficient for the planned stock level and working space.",
    "feed": "Secure a dependable feed supply and calculate feed cost for the full production cycle.",
    "fodder": "Secure year-round fodder availability and a lean-season backup before increasing herd size.",
    "grazing": "Confirm safe grazing access or an alternative fodder plan for the entire production period.",
    "veterinary": "Arrange dependable veterinary support and a preventive health/vaccination schedule before stocking.",
    "electricity": "Confirm reliable electricity or a suitable backup power arrangement for the selected equipment.",
    "equipment": "Confirm the required equipment, capacity, maintenance plan and supplier support before investment.",
    "tools": "Confirm the required tools and keep a basic replacement/maintenance plan before starting operations.",
    "machine": "Confirm machine capacity, installation, operator training and maintenance support before purchase.",
    "grinder": "Confirm grinder capacity, power requirement, maintenance and safe operating procedures before purchase.",
    "packaging": "Finalize food-safe packaging, labeling and a costed packaging supply chain before commercial sales.",
    "raw_material": "Confirm a reliable raw-material supply and at least one backup supplier before scaling.",
    "supplier_network": "Build a dependable supplier network and keep an alternative supplier for critical stock.",
    "workspace": "Confirm a suitable workspace with enough operating area, ventilation, storage and customer/service access.",
    "workshop": "Confirm a safe workshop, essential tools, power supply and maintenance workspace before launch.",
    "shop": "Confirm a suitable customer-facing shop location, storage area and basic operating setup before stocking.",
    "vehicle": "Confirm vehicle availability, operating cost, route plan and a backup arrangement before accepting regular work.",
    "driver": "Confirm a reliable licensed driver/operator and define working hours and route responsibilities before launch.",
    "fuel": "Budget fuel and maintenance costs and confirm a dependable refuelling plan for regular operations.",
    "skill": "Strengthen the core service skill through practical training and supervised work before scaling.",
    "technical_skill": "Arrange technical training or an experienced technician for installation, diagnosis and repair work.",
    "spares": "Maintain a basic stock of frequently required spare parts and identify reliable suppliers.",
    "service_area": "Define the practical service radius and transport time so customer response remains reliable.",
    "farmer_demand": "Validate demand with local farmers/service buyers before purchasing equipment or carrying inventory.",
    "plant_material": "Source verified planting material and confirm nursery survival/quality checks before expanding production.",
    "shade": "Provide suitable shade/protection and control heat and moisture conditions for nursery stock.",
    "water_quality": "Test water quality and correct unsuitable parameters before stocking or using the water system.",
    "risk": "Identify the main risk for this activity and put the relevant prevention or contingency step in place before scaling.",
    "drying": "Confirm a clean, protected drying area and a practical drying schedule that preserves product quality.",
    "protected": "Confirm suitable protected cultivation infrastructure and verify that its cost is justified at the planned scale.",
    "long_term": "Confirm that the longer production timeline fits your cash-flow plan and that you can maintain the activity until harvest.",
    "birds": "Confirm the planned bird capacity, shed space, feed, water and health-management arrangements before stocking.",
    "animals": "Confirm the planned animal capacity against dependable housing, feed, water and health-support resources.",
    "animal_type": "Choose the animal type only after checking local climate, feed availability, housing and buyer demand.",
    "operator": "Confirm a reliable operator with the skills needed to run the selected equipment or service safely.",
    "vehicle_type": "Choose a vehicle type that matches the payload, route, road conditions and operating cost of the service.",
    "space": "Confirm sufficient usable space for the selected activity, including working and storage areas.",
    "room_area": "Confirm adequate room area and layout for the planned production capacity.",
    "temperature_control": "Confirm practical temperature-control equipment and monitoring before starting temperature-sensitive production.",
    "humidity_control": "Confirm practical humidity-control and monitoring arrangements before starting humidity-sensitive production.",
    "substrate": "Secure suitable substrate material and a consistent preparation/supply process before scaling production.",
    "rearing_space": "Confirm adequate rearing space, hygiene and ventilation for the planned production scale.",
    "mulberry_land": "Confirm enough mulberry area to support the planned silkworm batch size and maintain a dependable leaf supply.",
    "oilseed_supply": "Confirm a reliable oilseed supply and quality-check process before scaling oil extraction.",
    "workspace": "Confirm a suitable workspace with adequate operating area, ventilation, safety and storage.",
    "water_source": "Confirm the water source, reliability and refill/management plan before stocking the system.",
    "pond_type": "Verify pond type, depth, drainage and water-retention suitability before stocking.",
    "species": "Select the species based on the location, water conditions, climate and confirmed local market demand.",
    "forage": "Confirm adequate forage/flower availability throughout the production season before stocking.",
    "boxes": "Confirm enough boxes/hives and a suitable placement area before expanding colony numbers.",
    "rearing_space": "Confirm adequate rearing space, hygiene and ventilation for the planned production scale.",
    "milk_supply": "Confirm dependable milk supply and collection/quality arrangements before expanding processing capacity.",
    "oilseed_supply": "Confirm a reliable local oilseed supply and quality-testing process before scaling processing.",
    "cold_storage": "Confirm cold storage or a fast-turnover distribution plan for products that require temperature control.",
}

BUSINESS_GAP_ACTIONS_TR = {
    "Hindi": {
        "market_access":"इस व्यवसाय के लिए कम से कम दो वास्तविक खरीदार चैनल सुनिश्चित करें और हर बिक्री चक्र से पहले कीमतों की तुलना करें।",
        "water":"योजनाबद्ध स्तर के लिए भरोसेमंद पानी का स्रोत और एक वैकल्पिक व्यवस्था शुरू करने से पहले सुनिश्चित करें।",
        "irrigation":"चयनित गतिविधि के अनुसार भरोसेमंद सिंचाई या पानी की आपूर्ति की व्यावहारिक योजना बनाएं।",
        "land_acres":"उपलब्ध उपयोगी भूमि क्षेत्र की पुष्टि करें और योजना को उपलब्ध क्षेत्र के भीतर रखें।",
        "investment":"शुरू करने से पहले पूरी प्रारंभिक और कार्यशील पूंजी का बजट तथा आकस्मिक राशि तैयार करें।",
        "labour":"सबसे व्यस्त अवधि के लिए भरोसेमंद श्रमिकों की व्यवस्था करें और वैकल्पिक सहायता रखें।",
        "experience":"पायलट से आगे बढ़ने से पहले व्यावहारिक प्रशिक्षण लें या अनुभवी ऑपरेटर के साथ काम करें।",
        "soil_test":"हाल की मिट्टी जांच कराएं और उसके परिणाम से फसल तथा पोषक तत्वों की योजना बनाएं।",
        "transport":"उत्पादन या बिक्री शुरू होने से पहले भरोसेमंद परिवहन और संग्रह/डिलीवरी योजना तय करें।",
        "storage":"खराब होने, नुकसान और गुणवत्ता में कमी को रोकने के लिए उचित भंडारण और हैंडलिंग की व्यवस्था करें।",
        "shed":"पशु या पक्षी रखने से पहले उचित शेड, वेंटिलेशन, जल निकासी और स्वच्छता पूरी करें।",
        "feed":"भरोसेमंद चारा आपूर्ति सुनिश्चित करें और पूरे उत्पादन चक्र की चारा लागत की गणना करें।",
        "veterinary":"पशु रखने से पहले भरोसेमंद पशु-चिकित्सा सहायता और स्वास्थ्य/टीकाकरण कार्यक्रम तय करें।",
        "electricity":"उपकरणों के लिए भरोसेमंद बिजली या उपयुक्त बैकअप पावर की व्यवस्था सुनिश्चित करें।",
        "equipment":"निवेश से पहले आवश्यक उपकरण, क्षमता, रखरखाव और सप्लायर सहायता की पुष्टि करें।",
        "raw_material":"स्केल बढ़ाने से पहले भरोसेमंद कच्चे माल की आपूर्ति और कम से कम एक वैकल्पिक सप्लायर तय करें।",
        "workspace":"पर्याप्त कार्यक्षेत्र, वेंटिलेशन, भंडारण और ग्राहक/सेवा पहुंच वाला उपयुक्त स्थान सुनिश्चित करें।",
        "vehicle":"नियमित काम लेने से पहले वाहन, संचालन लागत, रूट और बैकअप व्यवस्था सुनिश्चित करें।",
        "skill":"स्केल बढ़ाने से पहले मुख्य सेवा कौशल को व्यावहारिक प्रशिक्षण और पर्यवेक्षित काम से मजबूत करें।",
        "technical_skill":"तकनीकी प्रशिक्षण या अनुभवी तकनीशियन की सहायता स्थापना, जांच और मरम्मत के लिए सुनिश्चित करें।",
        "spares":"अक्सर लगने वाले स्पेयर पार्ट्स का मूल स्टॉक रखें और भरोसेमंद सप्लायर तय करें।",
        "farmer_demand":"उपकरण या स्टॉक खरीदने से पहले स्थानीय किसानों/सेवा खरीदारों से मांग की पुष्टि करें।",
        "plant_material":"उत्पादन बढ़ाने से पहले प्रमाणित पौध सामग्री और गुणवत्ता/जीवित रहने की जांच सुनिश्चित करें।",
        "shade":"नर्सरी पौधों के लिए उचित छाया/सुरक्षा और तापमान व नमी नियंत्रण उपलब्ध कराएं।",
        "water_quality":"स्टॉकिंग या पानी की प्रणाली उपयोग करने से पहले पानी की गुणवत्ता जांचें और अनुपयुक्त मानकों को ठीक करें।",
        "species":"स्थान, पानी, जलवायु और स्थानीय बाजार मांग के आधार पर प्रजाति चुनें।",
    },
    "Kannada": {
        "market_access":"ಈ ವ್ಯವಹಾರಕ್ಕೆ ಕನಿಷ್ಠ ಎರಡು ನೈಜ ಖರೀದಿದಾರರ ಮಾರ್ಗಗಳನ್ನು ಖಚಿತಪಡಿಸಿ ಮತ್ತು ಪ್ರತಿ ಮಾರಾಟ ಚಕ್ರಕ್ಕೂ ಮೊದಲು ಬೆಲೆಗಳನ್ನು ಹೋಲಿಸಿ।",
        "water":"ಯೋಜಿತ ಮಟ್ಟಕ್ಕೆ ವಿಶ್ವಾಸಾರ್ಹ ನೀರಿನ ಮೂಲ ಮತ್ತು ಪರ್ಯಾಯ ವ್ಯವಸ್ಥೆಯನ್ನು ಆರಂಭಿಸುವ ಮೊದಲು ಖಚಿತಪಡಿಸಿ।",
        "irrigation":"ಆಯ್ಕೆ ಮಾಡಿದ ಚಟುವಟಿಕೆಗೆ ಸೂಕ್ತವಾದ ವಿಶ್ವಾಸಾರ್ಹ ನೀರಾವರಿ ಅಥವಾ ನೀರು ಪೂರೈಕೆ ಯೋಜನೆ ರೂಪಿಸಿ।",
        "land_acres":"ಲಭ್ಯವಿರುವ ಬಳಕೆಯ ಭೂಮಿಯ ವಿಸ್ತೀರ್ಣವನ್ನು ಖಚಿತಪಡಿಸಿ ಮತ್ತು ಯೋಜನೆಯನ್ನು ಅದಕ್ಕೆ ಹೊಂದಿಸಿ।",
        "investment":"ಆರಂಭಿಸುವ ಮೊದಲು ಸಂಪೂರ್ಣ ಆರಂಭಿಕ ಮತ್ತು ಕಾರ್ಯನಿರ್ವಹಣಾ ಬಂಡವಾಳದ ಬಜೆಟ್ ಹಾಗೂ ತುರ್ತು ಮೀಸಲನ್ನು ಸಿದ್ಧಪಡಿಸಿ।",
        "labour":"ಅತ್ಯಂತ ಬ್ಯುಸಿ ಅವಧಿಗೆ ವಿಶ್ವಾಸಾರ್ಹ ಕಾರ್ಮಿಕರನ್ನು ವ್ಯವಸ್ಥೆ ಮಾಡಿ ಮತ್ತು ಪರ್ಯಾಯ ಸಹಾಯವನ್ನು ಇರಿಸಿ।",
        "experience":"ಪೈಲಟ್ ಹಂತದ ನಂತರ ವಿಸ್ತರಿಸುವ ಮೊದಲು ಪ್ರಾಯೋಗಿಕ ತರಬೇತಿ ಪಡೆಯಿರಿ ಅಥವಾ ಅನುಭವಿ ನಿರ್ವಾಹಕರೊಂದಿಗೆ ಕೆಲಸ ಮಾಡಿ।",
        "soil_test":"ಇತ್ತೀಚಿನ ಮಣ್ಣಿನ ಪರೀಕ್ಷೆ ಮಾಡಿಸಿ ಅದರ ಫಲಿತಾಂಶದ ಆಧಾರದ ಮೇಲೆ ಬೆಳೆ ಮತ್ತು ಪೋಷಕಾಂಶ ಯೋಜನೆ ಮಾಡಿ।",
        "transport":"ಉತ್ಪಾದನೆ ಅಥವಾ ಮಾರಾಟ ಆರಂಭಿಸುವ ಮೊದಲು ವಿಶ್ವಾಸಾರ್ಹ ಸಾರಿಗೆ ಮತ್ತು ಸಂಗ್ರಹ/ವಿತರಣಾ ಯೋಜನೆ ಖಚಿತಪಡಿಸಿ।",
        "storage":"ಹಾಳಾಗುವಿಕೆ, ನಷ್ಟ ಮತ್ತು ಗುಣಮಟ್ಟ ಕುಸಿತ ಕಡಿಮೆ ಮಾಡಲು ಸೂಕ್ತ ಸಂಗ್ರಹಣೆ ಮತ್ತು ಹ್ಯಾಂಡ್ಲಿಂಗ್ ವ್ಯವಸ್ಥೆ ಮಾಡಿ।",
        "shed":"ಪ್ರಾಣಿಗಳು ಅಥವಾ ಪಕ್ಷಿಗಳನ್ನು ಇರಿಸುವ ಮೊದಲು ಸೂಕ್ತ ಶೆಡ್, ಗಾಳಿ ಹರಿವು, ನೀರು ಹರಿವು ಮತ್ತು ಸ್ವಚ್ಛತೆ ವ್ಯವಸ್ಥೆ ಪೂರ್ಣಗೊಳಿಸಿ।",
        "feed":"ವಿಶ್ವಾಸಾರ್ಹ ಆಹಾರ/ಮೇವು ಪೂರೈಕೆ ಖಚಿತಪಡಿಸಿ ಮತ್ತು ಸಂಪೂರ್ಣ ಉತ್ಪಾದನಾ ಚಕ್ರದ ವೆಚ್ಚ ಲೆಕ್ಕಿಸಿ।",
        "veterinary":"ಪ್ರಾಣಿಗಳನ್ನು ಇರಿಸುವ ಮೊದಲು ವಿಶ್ವಾಸಾರ್ಹ ಪಶುವೈದ್ಯಕೀಯ ನೆರವು ಮತ್ತು ಆರೋಗ್ಯ/ಲಸಿಕೆ ವೇಳಾಪಟ್ಟಿ ಸಿದ್ಧಪಡಿಸಿ।",
        "electricity":"ಉಪಕರಣಗಳಿಗೆ ವಿಶ್ವಾಸಾರ್ಹ ವಿದ್ಯುತ್ ಅಥವಾ ಸೂಕ್ತ ಬ್ಯಾಕಪ್ ವಿದ್ಯುತ್ ವ್ಯವಸ್ಥೆ ಖಚಿತಪಡಿಸಿ।",
        "equipment":"ಹೂಡಿಕೆಗೆ ಮೊದಲು ಅಗತ್ಯ ಉಪಕರಣ, ಸಾಮರ್ಥ್ಯ, ನಿರ್ವಹಣೆ ಮತ್ತು ಪೂರೈಕೆದಾರರ ನೆರವು ಖಚಿತಪಡಿಸಿ।",
        "raw_material":"ವಿಸ್ತರಿಸುವ ಮೊದಲು ವಿಶ್ವಾಸಾರ್ಹ ಕಚ್ಚಾ ವಸ್ತು ಪೂರೈಕೆ ಮತ್ತು ಕನಿಷ್ಠ ಒಂದು ಪರ್ಯಾಯ ಪೂರೈಕೆದಾರರನ್ನು ಖಚಿತಪಡಿಸಿ।",
        "workspace":"ಸಾಕಷ್ಟು ಕೆಲಸದ ಸ್ಥಳ, ಗಾಳಿ ಹರಿವು, ಸಂಗ್ರಹಣೆ ಮತ್ತು ಗ್ರಾಹಕ/ಸೇವಾ ಪ್ರವೇಶ ಇರುವ ಸ್ಥಳವನ್ನು ಖಚಿತಪಡಿಸಿ।",
        "vehicle":"ನಿಯಮಿತ ಕೆಲಸ ಸ್ವೀಕರಿಸುವ ಮೊದಲು ವಾಹನ, ನಿರ್ವಹಣಾ ವೆಚ್ಚ, ಮಾರ್ಗ ಮತ್ತು ಬ್ಯಾಕಪ್ ವ್ಯವಸ್ಥೆ ಖಚಿತಪಡಿಸಿ।",
        "skill":"ವಿಸ್ತರಿಸುವ ಮೊದಲು ಮುಖ್ಯ ಸೇವಾ ಕೌಶಲ್ಯವನ್ನು ಪ್ರಾಯೋಗಿಕ ತರಬೇತಿ ಮತ್ತು ಮೇಲ್ವಿಚಾರಿತ ಕೆಲಸದಿಂದ ಬಲಪಡಿಸಿ।",
        "technical_skill":"ಸ್ಥಾಪನೆ, ಪರಿಶೀಲನೆ ಮತ್ತು ದುರಸ್ತಿಗಾಗಿ ತಾಂತ್ರಿಕ ತರಬೇತಿ ಅಥವಾ ಅನುಭವಿ ತಂತ್ರಜ್ಞರ ನೆರವು ಪಡೆಯಿರಿ।",
        "spares":"ಹೆಚ್ಚಾಗಿ ಬೇಕಾಗುವ ಸ್ಪೇರ್ ಭಾಗಗಳ ಮೂಲ ಸ್ಟಾಕ್ ಇಟ್ಟು ವಿಶ್ವಾಸಾರ್ಹ ಪೂರೈಕೆದಾರರನ್ನು ಗುರುತಿಸಿ।",
        "farmer_demand":"ಉಪಕರಣ ಅಥವಾ ಸ್ಟಾಕ್ ಖರೀದಿಸುವ ಮೊದಲು ಸ್ಥಳೀಯ ರೈತರು/ಸೇವಾ ಖರೀದಿದಾರರ ಬೇಡಿಕೆಯನ್ನು ಪರಿಶೀಲಿಸಿ।",
        "plant_material":"ವಿಸ್ತರಣೆಗೆ ಮೊದಲು ಪ್ರಮಾಣಿತ ನೆಡುವ ವಸ್ತು ಮತ್ತು ಗುಣಮಟ್ಟ/ಬದುಕುಳಿಯುವಿಕೆ ಪರಿಶೀಲನೆ ಖಚಿತಪಡಿಸಿ।",
        "shade":"ನರ್ಸರಿ ಸಸಿಗಳಿಗೆ ಸೂಕ್ತ ನೆರಳು/ರಕ್ಷಣೆ ಮತ್ತು ತಾಪಮಾನ-ತೇವಾಂಶ ನಿಯಂತ್ರಣ ಒದಗಿಸಿ।",
        "water_quality":"ಸ್ಟಾಕಿಂಗ್ ಅಥವಾ ನೀರಿನ ವ್ಯವಸ್ಥೆ ಬಳಸುವ ಮೊದಲು ನೀರಿನ ಗುಣಮಟ್ಟ ಪರೀಕ್ಷಿಸಿ ಮತ್ತು ಸಮಸ್ಯೆಗಳನ್ನು ಸರಿಪಡಿಸಿ।",
        "species":"ಸ್ಥಳ, ನೀರು, ಹವಾಮಾನ ಮತ್ತು ಸ್ಥಳೀಯ ಮಾರುಕಟ್ಟೆ ಬೇಡಿಕೆಗೆ ಅನುಗುಣವಾಗಿ ಜಾತಿಯನ್ನು ಆಯ್ಕೆ ಮಾಡಿ।",
    }
}

def business_gap_action(field_key):
    lang = _current_language()
    if lang in BUSINESS_GAP_ACTIONS_TR and field_key in BUSINESS_GAP_ACTIONS_TR[lang]:
        return BUSINESS_GAP_ACTIONS_TR[lang][field_key]
    action = BUSINESS_GAP_ACTIONS.get(field_key)
    if action:
        return action
    label = tr_any(FIELD_LABELS.get(field_key, field_key.replace("_", " ").title()))
    if lang == "Hindi":
        return f"इस व्यवसाय को बढ़ाने से पहले {label} की आवश्यक व्यवस्था सुनिश्चित करें और इसकी क्षमता/उपलब्धता की पुष्टि करें।"
    if lang == "Kannada":
        return f"ಈ ವ್ಯವಹಾರವನ್ನು ವಿಸ್ತರಿಸುವ ಮೊದಲು {label} ಅಗತ್ಯ ವ್ಯವಸ್ಥೆಯನ್ನು ಖಚಿತಪಡಿಸಿ ಮತ್ತು ಅದರ ಸಾಮರ್ಥ್ಯ/ಲಭ್ಯತೆಯನ್ನು ಪರಿಶೀಲಿಸಿ."
    return f"Confirm the required {label} arrangement and its capacity/availability before scaling this business."

def _business_field_is_gap(field_key, value):
    if value is None or (isinstance(value, str) and value.strip() in {"", "Not sure", "Unknown", "Not provided"}):
        return True
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value) <= 0
    low = {"none", "no", "poor", "very low", "low", "limited", "partial", "beginner"}
    return str(value).strip().lower() in low

def business_priority_gaps(business_name, values):
    """Return only gaps that belong to the currently selected business.
    The business configuration supplies the weighted fields, so changing the
    selected activity automatically changes this list and its actions.
    """
    _, cfg = business_config_for(business_name)
    if not cfg:
        return []
    gaps = []
    # Preserve business-config order so the most important weighted factors
    # appear first.
    for field_key in cfg.get("weights", {}):
        value = values.get(field_key)
        if not _business_field_is_gap(field_key, value):
            continue
        label = FIELD_LABELS.get(field_key, field_key.replace("_", " ").title())
        gaps.append((field_key, label))
    # Never show a generic "missing inputs" sentence here. If every configured
    # factor is currently satisfactory, the business has no priority gap.
    return gaps[:6]

def gap_specific_action(gap_text):
    """Map a priority-gap description to a concrete, gap-specific next action,
    instead of showing the same generic sentence for every row."""
    g = str(gap_text).lower()
    rules = [
        ("missing or unknown inputs", "Go back to Step 2 and fill in the listed fields with your best real estimate; the score updates once they are entered."),
        ("water availability", "Arrange a dependable water source (borewell, canal, tank or a rainwater-harvesting plan) sized for the chosen scale before committing capital."),
        ("irrigation", "Upgrade irrigation reliability (drip/sprinkler or a scheduled water source) so supply is not left to rainfall alone."),
        ("land area", "Confirm the exact usable land/covered area, including access and boundary, before planning input quantities."),
        ("investment", "Build a phased investment plan: start with the pilot-scale amount and add a contingency buffer of 10-15%."),
        ("capital", "Build a phased investment plan: start with the pilot-scale amount and add a contingency buffer of 10-15%."),
        ("market access", "Identify and confirm at least two realistic buyers (mandi, retailer, FPO or direct customers) before scaling production."),
        ("labour", "Line up reliable labour (family, hired or shared) for the peak activity periods before starting."),
        ("season", "Align sowing and production timing with the locally appropriate Kharif, Rabi or Summer window for the chosen crop."),
        ("soil test", "Get a soil test done at the nearest Krishi Vigyan Kendra / Soil Health Card centre and use the results to plan fertiliser dosage."),
        ("soil ph", "Adjust soil pH toward the crop's preferred band using lime (for acidic soil) or gypsum/organic matter (for alkaline soil), based on a soil test."),
        ("nitrogen", "Apply nitrogen-rich fertiliser or compost in line with the crop's recommended dose after a soil test."),
        ("phosphorus", "Apply phosphorus-rich fertiliser (e.g. DAP/SSP) in line with the crop's recommended dose after a soil test."),
        ("potassium", "Apply potash-based fertiliser in line with the crop's recommended dose after a soil test."),
        ("temperature", "Choose crop varieties and sowing windows suited to the location's expected temperature range."),
        ("humidity", "Plan disease and pest monitoring appropriate to the location's humidity level, especially during high-humidity periods."),
        ("rainfall", "Plan supplemental irrigation or drainage to cover gaps between the crop's water need and expected rainfall."),
        ("experience", "Take a short training course or attach with an experienced farmer/operator before scaling up this activity."),
        ("electricity", "Confirm a reliable power connection or a backup (generator/solar pump) for pumps and processing equipment."),
        ("veterinary", "Register with a nearby veterinary service or animal-health worker for routine check-ups and emergencies."),
        ("transport", "Arrange transport (own, shared or hired) so produce reaches the market without spoilage or delay."),
        ("storage", "Arrange basic storage (dry, cold or covered as needed) to reduce post-harvest and post-production losses."),
        ("shed", "Build or upgrade housing/shed space appropriate to the planned number of animals or birds before stocking."),
        ("feed", "Confirm a reliable feed/fodder supply chain, including a plan for lean-season shortages."),
        ("fodder", "Confirm a reliable feed/fodder supply chain, including a plan for lean-season shortages."),
        ("grazing", "Confirm a reliable feed/fodder supply chain, including a plan for lean-season shortages."),
        ("income", "Re-check whether this business's typical time-to-income fits your cash-flow needs; plan a bridge income source if it does not."),
        ("risk", "Choose a risk-management step (insurance, diversification or a smaller pilot) that matches your risk preference."),
    ]
    for keyword, action in rules:
        if keyword in g:
            return action
    return "Close this gap or test a smaller pilot before scaling."


def business_specific_output(name, domain_name, cfg, values, score, reasons, gaps, location):
    """Render the strategic dashboard with a compact, production-style information hierarchy."""
    schemes = schemes_for_business(name)
    profile = _profile_for_business(name)
    options = _option_candidates(name, domain_name, location)
    advice = BUSINESS_ADVICE.get(name, {}).get("advice", DEFAULT_ADVICE)
    steps = BUSINESS_ADVICE.get(name, {}).get("steps", DEFAULT_STEPS)

    # Financial figures are explicitly labelled estimates.
    capex = values.get("investment") or values.get("capital")
    break_even = "Not estimated"
    monthly_cost = "Not estimated"
    if profile:
        fm = business_financial_model(profile)
        plan_investment = float(capex or fm["recommended_investment"])
        proj = financial_projection(profile, plan_investment)
        be_lo, be_hi = proj["break_even"]
        if math.isfinite(be_lo) and math.isfinite(be_hi):
            break_even = f"{be_lo:.1f}–{be_hi:.1f} months"
        monthly_cost = f"₹{proj['cost'][0]:,.0f}–₹{proj['cost'][1]:,.0f}"
    capex_label = f"₹{float(capex):,.0f}" if capex else "Not provided"

    st.markdown(f"## 🔎 {tr_any(name)}")
    st.caption(f"{tr_any(domain_name)}  •  {tr_any(location)}  •  {tr_any('Rule-based feasibility assessment')}")
    chosen_product = values.get("species_product", "Not selected")
    if chosen_product and str(chosen_product) != "Not selected":
        st.success(f"🎯 {tr_any('Selected Species / Variety / Product')}: **{tr_any(chosen_product)}**")
    location_temp, location_temp_source = get_location_temperature(location)
    st.info(f"🌡️ {tr_any('Location temperature')}: **{location_temp:.1f} °C** · {tr_any(location_temp_source)}")
    st.divider()

    # Executive KPI header.
    k1,k2,k3,k4 = st.columns(4)
    with k1:
        st.markdown(f'<div class="gs-metric"><div class="label">{tr_any("CAPEX Required")}</div><div class="value">{capex_label}</div><div class="hint">{tr_any("Current input / configured estimate")}</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="gs-metric"><div class="label">{tr_any("Break-Even Timeline")}</div><div class="value">{break_even}</div><div class="hint">{tr_any("Indicative model estimate")}</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="gs-metric"><div class="label">{tr_any("Feasibility Score")}</div><div class="value">{score}/100</div><div class="hint">{tr_any("Adaptive score from available inputs")}</div></div>', unsafe_allow_html=True)
    with k4:
        st.markdown(f'<div class="gs-metric"><div class="label">{tr_any("Monthly Operating Cost")}</div><div class="value">{monthly_cost}</div><div class="hint">{tr_any("Indicative, scale-dependent")}</div></div>', unsafe_allow_html=True)
    st.caption(tr_any("Financial figures are planning estimates, not guarantees. Validate local supplier quotes, buyer prices and current scheme rules before committing capital."))

    tabs = st.tabs(["🌱 " + tr_any("Selection"), "🪜 " + tr_any("Execution Roadmap"), "🛒 " + tr_any("Market & Advisory"), "⚠️ " + tr_any("Risk Control"), "📊 " + tr_any("Financial Benchmarks"), "🏛️ " + tr_any("Schemes")])

    with tabs[0]:
        st.markdown("### " + tr_any("Species / Variety / Product Selection"))
        if domain_name == "Agriculture":
            matrix=[]
            for category, crop_list in options:
                for crop in crop_list:
                    profile_crop=CROP_PROFILES.get(crop,{})
                    matrix.append([
                        category, crop,
                        profile_crop.get("duration","Not available"),
                        profile_crop.get("soil","Not available"),
                        profile_crop.get("water","Not available"),
                        profile_crop.get("yield","Indicative; verify locally"),
                    ])
            if matrix:
                _md_table(["Category","Option","Cycle","Soil / space","Water","Indicative production"], matrix[:18])
                if len(matrix)>18:
                    st.caption(f"Showing 18 of {len(matrix)} location-suitable options in this dashboard. The full location mapping remains the source list.")
            else:
                st.info(tr_any("No location-suitable options are configured for this activity yet."))
            st.info(tr_any("Location filter") + f": {tr_place(location)}. " + tr_any("The candidate list comes from the prototype's location-to-crop mapping; feasibility is then assessed from the inputs you supplied."))
        else:
            matrix=[]
            for _, opt_items in options:
                for opt in opt_items:
                    if isinstance(opt, dict):
                        matrix.append([opt.get("name","—"),opt.get("cycle","—"),opt.get("space","—"),opt.get("climate","—"),opt.get("market","—")])
                    else:
                        matrix.append([str(opt),"—","—","—","—"])
            if matrix:
                _md_table(["Specific option","Production cycle","Space requirement","Climate compatibility","Target market"], matrix)
            else:
                st.info(tr_any("No business-specific selection library is configured for this activity yet."))

    with tabs[1]:
        st.markdown("### 🪜 " + tr_any("Execution Roadmap"))
        st.caption(tr_any("Prepare → pilot → validate → scale. Each phase has a clear outcome and a go/no-go gate."))
        roadmap = [
            ("01","Foundation & Setup","READY THE BUSINESS","Weeks 1–2","Make the site, resources, budget and compliance setup ready",["Confirm land / workspace, water and access conditions.","Prepare a minimum investment plan and cash buffer.","Complete required permits, registrations, testing or local checks."],"Gate 1 · Site + resources + budget confirmed","#2E7D32","#E8F5E9"),
            ("02","Procure & Pilot","TEST BEFORE SCALE","Weeks 3–8","Run a controlled pilot using the selected option and record real costs",["Procure quality inputs / stock / equipment from traceable suppliers.","Start with a manageable pilot size and track labour, water and input use.","Record production, quality, demand and actual spending."],"Gate 2 · Pilot data meets the planned operating thresholds","#558B2F","#F1F8E9"),
            ("03","Production, Market & Scale","TURN THE PILOT INTO A BUSINESS","After pilot validation","Move into repeat production, secure buyers and scale only where unit economics work",["Lock B2B + D2C sales channels and define pricing / pack strategy.","Schedule production, grading, storage and transport.","Review monthly cash flow and expand capacity in controlled steps."],"Gate 3 · Repeat demand + workable unit economics + operational control","#1B5E20","#E8F5E9"),
        ]
        for i,(no,title,tag,duration,goal,checks,gate,color,accent) in enumerate(roadmap):
            checks_html = "".join(["<div class='gs-roadmap-check'><span>✓</span><span>" + tr_any(c) + "</span></div>" for c in checks])
            connector = "<div class='gs-roadmap-connector'></div>" if i < 2 else ""
            html = "<div class='gs-roadmap-wrap'><div class='gs-roadmap-card' style='border-left-color:"+color+";'><div class='gs-roadmap-top'><div class='gs-roadmap-number' style='background:"+accent+";color:"+color+";'>"+no+"</div><div class='gs-roadmap-heading'><div class='gs-roadmap-tag' style='color:"+color+";'>"+tr_any(tag)+"</div><div class='gs-roadmap-title'>"+tr_any(title)+"</div></div><div class='gs-roadmap-duration'>⏱ "+tr_any(duration)+"</div></div><div class='gs-roadmap-goal'><b>"+tr_any("Outcome:")+"</b> "+tr_any(goal)+".</div><div class='gs-roadmap-checks'>"+checks_html+"</div><div class='gs-roadmap-gate'>"+tr_any(gate)+"</div></div>"+connector+"</div>"
            st.markdown(html, unsafe_allow_html=True)
        st.markdown(f"<div class='gs-insight gs-roadmap-final'><div class='gs-roadmap-final-icon'>↗</div><div><b>{tr_any("Scale rule")}</b><br><span>{tr_any("Do not move straight from setup to full investment. Validate the pilot, actual operating cost and buyer response first.")}</span></div></div>", unsafe_allow_html=True)

    with tabs[2]:
        st.info(tr_any("Strategic fit: combine at least one B2B route with a direct or diversified selling channel where the business model allows it."))
        market_channels={
            "Poultry Farming":"Local retailers, restaurants, meat shops, institutions and direct households.",
            "Dairy Farming":"Milk collection centres, dairies, sweet shops, cafes, retailers and direct subscriptions.",
            "Goat Farming":"Livestock buyers, traders, butchers and direct buyers.",
            "Sheep Farming":"Livestock buyers, traders, butchers and institutional buyers where available.",
            "Fish Farming":"Fish retailers, wholesalers, restaurants, hotels and direct consumers.",
            "Vegetable Cultivation":"Retailers, restaurants, hotels, FPOs, farmers' markets and direct subscriptions.",
            "Fruit Cultivation":"Fruit retailers, wholesalers, processors, hotels and direct consumers.",
            "Mushroom Cultivation":"Restaurants, retailers, hotels and direct consumers.",
            "Plant Nursery":"Farmers, landscapers, gardeners, institutions and horticulture projects.",
        }
        _md_table(["Route","Practical use","Pricing focus"],[
            ["B2B",market_channels.get(name,"Local institutional, wholesale or business buyers."),"Compare net realized price after transport, handling and buyer deductions."],
            ["D2C", "Direct local households or end users where practical.", "Test pack size, convenience, quality and repeat-purchase potential."],
            ["Differentiation", "Quality, grading, reliability, packaging or verified production practices where relevant.", "Measure realized premium rather than assuming a premium."],
        ])
        for item in advice[:4]:
            st.markdown(f"- {tr_any(item)}")

    with tabs[3]:
        st.warning(tr_any("Biological, climatic and operational risks should be actively managed before scaling."))
        risks=dynamic_risk_analysis(name,cfg,values,score,location)
        counts={"High":0,"Medium":0,"Low":0}
        for r in risks:
            lvl=r.get("level","Low")
            counts[lvl if lvl in counts else "Low"]+=1
        total=sum(counts.values()) or 1
        high_pct=round(counts["High"]/total*100); med_pct=round(counts["Medium"]/total*100); low_pct=100-high_pct-med_pct
        a,b,c=st.columns(3)
        a.metric("🔴 " + tr_any("High Risk"),f"{high_pct}%",f"{counts['High']} {tr_any('identified')}")
        b.metric("🟠 " + tr_any("Medium Risk"),f"{med_pct}%",f"{counts['Medium']} {tr_any('identified')}")
        c.metric("🟢 " + tr_any("Low Risk"),f"{low_pct}%",f"{counts['Low']} {tr_any('identified')}")
        risk_rows=[[r.get("title","Risk"),r.get("level","Low"),r.get("impact","—"),r.get("mitigation","Monitor and manage before scaling.")] for r in risks]
        if risk_rows:
            _md_table([tr_any("Risk"),tr_any("Level"),tr_any("Impact"),tr_any("Control / mitigation")],[[tr_any(a),tr_any(b),tr_any(c),tr_any(d)] for a,b,c,d in risk_rows])
        else:
            st.info(tr_any("No configured risk items were returned for this activity."))
        priority_gaps = business_priority_gaps(name, values)
        st.markdown("### " + tr_any("Priority gaps"))
        if priority_gaps:
            _md_table(
                [tr_any("Gap"), tr_any("Action")],
                [[tr_any(label), business_gap_action(field_key)] for field_key, label in priority_gaps]
            )
        else:
            no_gap_msg = {
                "English": "No business-specific priority gaps were identified from the current inputs.",
                "Hindi": "वर्तमान इनपुट के आधार पर इस व्यवसाय की कोई प्राथमिकता कमी नहीं मिली।",
                "Kannada": "ಪ್ರಸ್ತುತ ಇನ್‌ಪುಟ್‌ಗಳ ಆಧಾರದ ಮೇಲೆ ಈ ವ್ಯವಹಾರಕ್ಕೆ ಯಾವುದೇ ಆದ್ಯತಾ ಕೊರತೆ ಕಂಡುಬಂದಿಲ್ಲ."
            }[_current_language()]
            st.success(no_gap_msg)

    with tabs[4]:
        st.markdown("### " + tr_any("Financial Benchmarks"))
        if profile:
            plan_investment=float(capex or business_financial_model(profile)["recommended_investment"])
            fm=business_financial_model(profile)
            proj=financial_projection(profile,plan_investment)
            _md_table(["Benchmark","Indicative value","Interpretation"],[
                ["Minimum configured investment",f"₹{fm['minimum_investment']:,.0f}","Prototype planning range; validate supplier/asset quotes."],
                ["Planned investment",f"₹{plan_investment:,.0f}","Based on the current input or configured recommendation."],
                ["Monthly operating cost",f"₹{proj['cost'][0]:,.0f}–₹{proj['cost'][1]:,.0f}","Scale-dependent estimate."],
                ["Annual benefit",f"₹{proj['annual_benefit'][0]:,.0f}–₹{proj['annual_benefit'][1]:,.0f}","Indicative model output, not guaranteed income."],
                ["Break-even",break_even,"Depends on realized contribution margin and sales/production volume."],
                ["Feasibility indicator",f"{score}/100","Rule-based fit score from currently available inputs."],
            ])
        else:
            _md_table(["Benchmark","Value","Note"],[["CAPEX",capex_label,"Validate with quotations."],["Feasibility",f"{score}/100","Adaptive rule-based score."],["Break-even","Not estimated","Needs a configured financial model for this activity."]])
        st.info(tr_any("Success benchmark: complete a pilot with recorded unit cost, output/service volume, realized selling price, wastage/mortality where relevant, and customer acquisition cost before expanding."))

    with tabs[5]:
        st.success(tr_any("Applicable scheme information is shown for the selected business mapping. Eligibility and support depend on current official guidelines."))
        if schemes:
            scheme_rows=[]
            for scheme in schemes:
                details=SCHEME_DETAILS.get(scheme,{})
                scheme_rows.append([
                    scheme,
                    details.get("what_it_is","Check the current official scheme guidelines."),
                    details.get("benefit","Check the current official scheme guidelines."),
                    details.get("eligibility","Eligibility depends on the current official guidelines."),
                    details.get("note","Prepare documents requested by the implementing authority or lender."),
                ])
            _md_table(["Scheme","What it supports","Financial assistance","Eligibility","Key documents / conditions"],scheme_rows)
            for scheme in schemes:
                src=SCHEME_DETAILS.get(scheme,{}).get("source")
                if src: st.caption(f"{scheme}: {src}")
        else:
            pass

    st.divider()
    st.markdown("### ✅ " + tr_any("Practical Decision Check"))
    if score>=75:
        st.success(tr_any("Several currently entered conditions support feasibility. Validate supplier quotes, operating costs and buyer demand before scaling."))
    elif score>=55:
        st.warning(tr_any("The current assessment is mixed. Close the highest-impact gaps and test a smaller pilot before committing the full investment."))
    else:
        st.warning(tr_any("Several configured conditions are weak. Address the highest-impact gaps first and reassess before committing the full investment."))


def apply_location_context_to_business_values(domain_name, values, location):
    """Use the globally selected location as the source of water and temperature context."""
    out=dict(values)
    ctx=LOCATION_CONTEXT.get(location,{})
    out["temperature"] = get_location_temperature(location)[0]
    if "water" in out or domain_name=="Agriculture":
        out["water"]=automatic_location_water(location)
    if "irrigation" in out and domain_name=="Agriculture":
        out["irrigation"]=automatic_location_irrigation(location)
    if domain_name=="Agriculture":
        if out.get("rainfall") in (None,"",0):
            out["rainfall"]=automatic_location_rainfall(location)
        if out.get("season") in (None,"",0):
            out["season"]=automatic_location_season()
        npk_defaults=None
        for k in ("nitrogen","phosphorus","potassium","soil_ph","humidity"):
            if out.get(k) in (None,"",0):
                if npk_defaults is None:
                    npk_defaults,_=automatic_location_soil_npk(location)
                src=({"nitrogen":"N","phosphorus":"P","potassium":"K","soil_ph":"soil_ph","humidity":"humidity"})[k]
                out[k]=npk_defaults.get(src,0.0)
    out["location"]=location
    return out

def agriculture_preflight_checks(business_name, values, location):
    """Catch common Agriculture-domain errors before the strategic dashboard."""
    issues, warnings=[],[]
    water=automatic_location_water(location)
    candidates=[]
    for _,items in _agriculture_options_for_business(business_name,location):
        candidates.extend([x for x in items if not str(x).startswith("No verified")])
    crop_businesses={"Vegetable Cultivation","Fruit Cultivation","Crop Cultivation","Cereals","Pulses","Oilseeds","Commercial Crops","Spice Cultivation"}
    loc_display = tr_place(location)
    if business_name in crop_businesses and not candidates:
        issues.append(f"No mapped {business_name.lower()} options are available for {loc_display}.")
    if business_name=="Vegetable Cultivation" and water in {"Limited","Low","None"}:
        issues.append(f"Vegetable cultivation has a {water.lower()} location-water profile at {loc_display}; reliable supplemental irrigation should be confirmed before scaling.")
    if business_name=="Fruit Cultivation" and water in {"Limited","Low","None"}:
        issues.append(f"Fruit cultivation has a {water.lower()} location-water profile at {loc_display}; orchard crops should not be scaled without a dependable water plan.")
    land=safe_float(values.get("land_acres",0)); investment=safe_float(values.get("investment",0)); labour=safe_float(values.get("labour",0)); market=str(values.get("market_access",""))
    if land<=0: warnings.append("Land area has not been entered yet.")
    if investment<=0: warnings.append("Available investment has not been entered yet.")
    if labour<1 and business_name in {"Vegetable Cultivation","Fruit Cultivation","Crop Cultivation","Spice Cultivation","Floriculture"}: warnings.append("At least one reliable labour resource should be planned for routine field operations.")
    if market=="Poor": warnings.append("Market access is set to Poor; confirm at least two buyers before scaling.")
    numeric_ranges={"nitrogen":(0,200),"phosphorus":(0,200),"potassium":(0,250),"temperature":(-5,55),"humidity":(0,100),"soil_ph":(3.5,10),"rainfall":(0,5000)}
    for key,(lo,hi) in numeric_ranges.items():
        if values.get(key) is None: continue
        try:
            x=float(values[key])
            # 0 is the intentional blank/default state for business numeric inputs.
            # Do not treat it as a real environmental measurement.
            if x == 0: continue
            if x<lo or x>hi: issues.append(f"{FIELD_LABELS.get(key,key)} value {x:g} is outside the supported planning range ({lo:g}–{hi:g}).")
        except Exception: issues.append(f"{FIELD_LABELS.get(key,key)} must be numeric.")
    env_results,env_source=agriculture_environment_analysis(location,business_name,values)
    invalid_env=[r for r in env_results if not r.get("valid")]
    if invalid_env: warnings.append(f"{len(invalid_env)} candidate crop option(s) fall outside the uploaded NPK/environment reference bands.")
    if env_results and env_source and "not found" in str(env_source).lower(): warnings.append("The NPK reference CSV is not available in this deployment, so environmental matching is limited to the location profile.")
    return issues,warnings,env_results

def show_agriculture_checks(business_name, values, location):
    issues,warnings,env_results=agriculture_preflight_checks(business_name,values,location)
    if issues:
        st.warning("⚠️ Agriculture input checks — review before scaling")
        for item in issues: st.markdown(f"- {tr_any(item)}")
    if warnings:
        st.warning("🔎 Agriculture checks / advisory notes")
        for item in warnings: st.markdown(f"- {tr_any(item)}")
    return issues,warnings,env_results

def rank_business_recommendations(domain_name, values, location, limit=3):
    """Return a rule-based shortlist using the existing business evaluator."""
    cfg = BUSINESS_DOMAIN_CONFIG.get(domain_name, {})
    businesses = cfg.get("businesses", {})
    ranked = []
    for business_name in businesses:
        try:
            local_values = dict(values)
            local_values["location"] = location
            score, reasons, gaps = evaluate_business_config(business_name, local_values)

            # Agriculture recommendations must respect the selected location.
            # Do not recommend vegetable/fruit/crop activities merely because
            # their generic input score is high when the location mapping has
            # no matching crop options or the location has limited water.
            if domain_name == "Agriculture":
                crop_businesses = {
                    "Vegetable Cultivation", "Fruit Cultivation", "Crop Cultivation",
                    "Cereals", "Pulses", "Oilseeds", "Commercial Crops",
                    "Spice Cultivation", "Floriculture"
                }
                if business_name in crop_businesses:
                    candidates = []
                    for _, items in _agriculture_options_for_business(business_name, location):
                        candidates.extend([x for x in items if not str(x).startswith("No verified")])
                    if not candidates and business_name != "Floriculture":
                        score -= 30
                        gaps.append(f"No mapped crop options for {tr_place(location)}.")
                    if business_name in {"Vegetable Cultivation", "Fruit Cultivation"} and automatic_location_water(location) in {"Limited", "Low", "None"}:
                        score -= 20
                        gaps.append(f"Location water is {automatic_location_water(location)}.")

            ranked.append({
                "business": business_name,
                "score": max(0, min(100, round(safe_float(score)))),
                "reasons": reasons,
                "gaps": gaps,
            })
        except Exception:
            continue
    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked[:limit]


# ============================================================
# BUSINESS RECOMMENDATION
# ============================================================

if page == "Business Recommendation":
    st.markdown(
        f'<div class="hero"><h1>💡 {tr_any("Business Recommendation")}</h1>'
        f'<p>{tr_any("Complete Step 1, then Step 2. Step 3 appears only after recommendations are generated and lets you select an activity for its strategic guidance and related schemes.")}</p></div>',
        unsafe_allow_html=True,
    )

    # STEP 1 — shown only where Step 1 content begins.
    st.markdown("## 1️⃣ " + tr_any("Step 1 — Select Business"))
    st.caption(tr_any("Choose the business domain and activity first. The selected location is reused automatically throughout this assessment."))

    domain_names = list(BUSINESS_DOMAIN_CONFIG.keys())
    c1, c2, c3 = st.columns([1.1, 1.5, 1])
    with c1:
        domain_name = st.selectbox("🏷️ " + tr_any("Business Domain"), domain_names, format_func=lambda x: f"{BUSINESS_DOMAIN_CONFIG[x]['icon']} {tr_any(x)}", key="br_domain")
    business_names = list(BUSINESS_DOMAIN_CONFIG[domain_name].get("businesses", {}).keys())
    with c2:
        business_name = st.selectbox("💼 " + tr_any("Business Activity"), business_names, format_func=tr_any, key="br_business")
    with c3:
        st.markdown(
            f'<div class="gs-metric"><div class="label">{tr_any("Location")}</div>'
            f'<div class="value" style="font-size:1.05rem">{html.escape(tr_place(location))}</div>'
            f'<div class="hint">{tr_any("Used automatically for this assessment")}</div></div>',
            unsafe_allow_html=True,
        )

    selection_signature = (domain_name, business_name, location)
    if st.session_state.get("br_selection_signature") != selection_signature:
        st.session_state["br_selection_signature"] = selection_signature
        st.session_state.pop("business_recommendation_result", None)
        st.session_state.pop("br_top3", None)
        st.session_state.pop("br_selected_business", None)

    cfg = BUSINESS_DOMAIN_CONFIG[domain_name]["businesses"][business_name]
    values = {}
    input_items = list(cfg.get("inputs", []))
    # These fields are now filled in automatically (location + date + the
    # uploaded NPK dataset), so they are never shown as editable widgets.
    AUTO_ENV_KEYS = {
        "water", "irrigation", "temperature", "season",
        "nitrogen", "phosphorus", "potassium", "soil_ph", "humidity", "rainfall",
        "land_acres", "land_size", "crop",
    }
    groups = {"location_climate": [], "soil_water": [], "capital_financial": []}
    for item in input_items:
        if len(item) < 4 or item[0] in AUTO_ENV_KEYS:
            continue
        groups.setdefault(_input_group(item[0]), []).append(item)
    if domain_name == "Agriculture":
        existing = {x[0] for x in input_items if len(x) >= 1}
        for item in AGRICULTURE_ENV_INPUTS:
            if item[0] not in existing and item[0] not in AUTO_ENV_KEYS:
                groups[_input_group(item[0])].append(item)

    st.divider()

    # STEP 2 — all automatically derived environmental inputs are grouped
    # inside Location & Climate Parameters.
    st.markdown("## 2️⃣ " + tr_any("Step 2 — Enter Inputs"))
    st.caption(tr_any("Numeric inputs start at 0 and text inputs start blank. Water, temperature, season and soil nutrients are taken automatically from the selected location."))

    auto_water = automatic_location_water(location)
    auto_irrigation = automatic_location_irrigation(location)
    auto_temperature, temperature_source = get_location_temperature(location)
    auto_season = automatic_location_season(location)
    auto_npk, npk_source = ({}, None)

    if domain_name == "Agriculture":
        state_crops = list(suitable_crops_for_location(location) or AGRI_LOCATION_CROPS.get(location, []))
        state_crops = list(dict.fromkeys(str(x) for x in state_crops if str(x).strip())) or ["Rice"]
        current_crop = st.session_state.get("agri_state_crop", state_crops[0])
        if current_crop not in state_crops: current_crop = state_crops[0]
        selected_crop = st.selectbox(
            "🌾 " + tr_any("Crop"), state_crops, index=state_crops.index(current_crop),
            key="agri_state_crop", format_func=tr_any,
            help=tr_any("Crop choices are automatically filtered for the selected state/UT."),
        )
        values["crop"] = selected_crop
        land_acres = st.number_input(
            "📐 " + tr_any("Land area (acres)"), min_value=0.1,
            value=float(st.session_state.get("agri_land_acres", 1.0)), step=0.5,
            key="agri_land_acres", help=tr_any("Enter usable agricultural land in acres."),
        )
        values["land_acres"] = float(land_acres)
        values["land_size"] = float(land_acres) * 0.404686
        st.caption(f"📍 {tr_any('Selected state/UT')}: {tr_place(location)} • 🗓️ {tr_any('Automatic season')}: {tr_any(auto_season)} • 🌾 {tr_any('State-specific crops')}: {len(state_crops)}")
        auto_npk, npk_source = automatic_location_soil_npk(location)
        values["season"] = auto_season
        values["nitrogen"] = auto_npk.get("N", 0.0)
        values["phosphorus"] = auto_npk.get("P", 0.0)
        values["potassium"] = auto_npk.get("K", 0.0)
        values["soil_ph"] = auto_npk.get("soil_ph", 0.0)
        values["humidity"] = auto_npk.get("humidity", 0.0)
        values["rainfall"] = auto_npk.get("rainfall", LOCATION_CONTEXT.get(location, {}).get("rainfall_mm", automatic_location_rainfall(location)))

    with st.expander("🌦️ " + tr_any("Location & Climate Parameters"), expanded=True):
        st.caption(tr_any("Location and climate automatically applied"))
        lc0, lc1, lc2, lc3 = st.columns(4)
        lc0.metric("📍 " + tr_any("Current location"), tr_place(location))
        lc1.metric("🌤️ " + tr_any("Climate"), tr_any(LOCATION_CONTEXT.get(location, {}).get("climate", "Moderate")))
        lc2.metric("🌡️ " + tr_any("Temperature"), f"{auto_temperature:.1f} °C")
        lc3.metric("🌧️ " + tr_any("Rainfall"), f"{automatic_location_rainfall(location):.0f} mm")
        if domain_name == "Agriculture":
            st.metric("📐 " + tr_any("Land area"), f"{float(values.get('land_acres', 1.0) or 1.0):.2f} acres")

        wc1, wc2 = st.columns(2)
        wc1.metric("💧 " + tr_any("Water availability"), tr_any(auto_water))
        wc2.metric("🚿 " + tr_any("Irrigation baseline"), tr_any(auto_irrigation))
        st.caption(f"🌡️ {tr_any('Temperature source')}: {tr_any(temperature_source)} • {tr_any('The temperature field is automatic and cannot be manually overridden.')}")

        if domain_name == "Agriculture":
            sc0, sc1, sc2, sc3, sc4, sc5 = st.columns(6)
            sc0.metric("🗓️ " + tr_any("Season"), tr_any(auto_season))
            sc1.metric("🧪 N", f"{auto_npk.get('N', 0):.0f}")
            sc2.metric("🧪 P", f"{auto_npk.get('P', 0):.0f}")
            sc3.metric("🧪 K", f"{auto_npk.get('K', 0):.0f}")
            sc4.metric("⚗️ " + tr_any("Soil pH"), f"{auto_npk.get('soil_ph', 0):.1f}")
            sc5.metric("💦 " + tr_any("Humidity"), f"{auto_npk.get('humidity', 0):.0f}%")
            if npk_source and "not found" not in str(npk_source).lower() and "unavailable" not in str(npk_source).lower():
                npk_note = tr_any("Soil nutrients (N-P-K), pH and humidity are averaged from the uploaded NPK dataset for crops typically grown at this location.")
            else:
                npk_note = tr_any("The uploaded NPK dataset was not found in this deployment, so soil nutrients are using safe planning defaults.")
            st.caption(f"🧬 {tr_any('Soil & season source')}: {npk_note} {tr_any('The season and soil fields are automatic and cannot be manually overridden.')}")

        card_cols = st.columns(3)
        for idx, item in enumerate(groups["location_climate"]):
            key, label, kind, opts = item
            with card_cols[idx % 3]:
                values[key] = render_business_input(key, label, kind, opts, widget_key=f"biz_{domain_name}_{business_name}_{key}")

    with st.expander("🎯 " + tr_any("Species / Variety / Product Selection"), expanded=True):
        selection_choices = business_selection_options(business_name, domain_name, location)
        st.caption(tr_any("Best context matches are shown first."))
        if domain_name == "Agriculture":
            values["species_product"] = values.get("crop", selection_choices[0] if selection_choices else "Not selected")
            st.markdown(f"**🌾 {tr_any('Selected crop')}:** {tr_any(str(values['species_product']))}")
        else:
            values["species_product"] = st.selectbox(
                tr_any("Species / Variety / Product Selection"),
                ["Not selected"] + selection_choices,
                index=1 if selection_choices else 0,
                key=f"biz_{domain_name}_{business_name}_{location}_species_product",
                help=tr_any("Choose the crop, animal type, fish species, nursery plant, processed product or service type you plan to work with."),
                format_func=tr_any,
            )
        if values["species_product"] != "Not selected":
            selected_detail = selection_detail_for(business_name, values["species_product"], domain_name, location)
            st.markdown("#### " + tr_any("Selected option details"))
            d1, d2, d3, d4 = st.columns(4)
            d1.metric("🎯 " + tr_any("Context fit"), f"{selected_detail['context_score']}/100")
            d2.metric("🌡️ " + tr_any("Climate"), tr_any(selected_detail["location_climate"]))
            d3.metric("💧 " + tr_any("Water requirement"), tr_any(str(selected_detail.get("water", selected_detail.get("location_water", "Activity-specific")))))
            d4.metric("📍 " + tr_any("Current location"), tr_place(location))
            _md_table(
                [tr_any("Why this option fits"), tr_any("Climate compatibility"), tr_any("Production / service cycle"), tr_any("Space / infrastructure"), tr_any("Typical market")],
                [[
                    ", ".join(selected_detail.get("reasons", [])),
                    selected_detail.get("climate", "—"),
                    selected_detail.get("cycle", "—"),
                    selected_detail.get("space", "—"),
                    selected_detail.get("market", "—"),
                ]]
            )

    with st.expander("🧪 " + tr_any("Soil & Water Profile"), expanded=True):
        card_cols = st.columns(3)
        for idx, item in enumerate(groups["soil_water"]):
            key, label, kind, opts = item
            with card_cols[idx % 3]:
                values[key] = render_business_input(key, label, kind, opts, widget_key=f"biz_{domain_name}_{business_name}_{key}")
    with st.expander("💰 " + tr_any("Capital & Financial Goals"), expanded=True):
        card_cols = st.columns(3)
        for idx, item in enumerate(groups["capital_financial"]):
            key, label, kind, opts = item
            with card_cols[idx % 3]:
                values[key] = render_business_input(key, label, kind, opts, widget_key=f"biz_{domain_name}_{business_name}_{key}")

    values = apply_location_context_to_business_values(domain_name, values, location)

    # ------------------------------------------------------------
    # GENERATE RECOMMENDATIONS + AGRICULTURE AI YIELD PREDICTION
    # ------------------------------------------------------------
    if st.button(
        "🔍 " + tr_any("Generate Business Recommendations"),
        type="primary",
        use_container_width=True,
        key="br_generate",
    ):
        # Generate the existing business shortlist for every domain.
        st.session_state["br_top3"] = rank_business_recommendations(
            domain_name,
            values,
            location,
            limit=3,
        )
        st.session_state.pop("br_selected_business", None)
        st.session_state.pop("business_recommendation_result", None)

        # Yield prediction is meaningful only for Agriculture.
        if domain_name == "Agriculture":
            try:
                state = str(location).strip().lower()
                crop_type = values.get("season", "Kharif")
                crop = values.get("crop") or values.get("species_product") or "Rice"
                rainfall = float(values.get("rainfall", 800) or 800)
                temperature = float(values.get("temperature", 25) or 25)
                acres = float(values.get("land_acres", st.session_state.get("agri_land_acres", 1.0)) or 1.0)
                area = acres * 0.404686

                if area <= 0:
                    raise ValueError("Land area must be greater than 0 acres.")

                input_df = pd.DataFrame({
                    "State_Name": [state],
                    "Crop_Type": [crop_type],
                    "Crop": [crop],
                    "rainfall": [rainfall],
                    "temperature": [temperature],
                    "Area_in_hectares": [area],
                })

                predicted_yield = float(yield_model.predict(input_df)[0])
                predicted_yield = max(0.0, predicted_yield)
                estimated_production = predicted_yield * area

                st.session_state["predicted_yield"] = predicted_yield
                st.session_state["estimated_production"] = estimated_production
                st.session_state["yield_inputs"] = {
                    "state": state,
                    "crop_type": crop_type,
                    "crop": crop,
                    "rainfall": rainfall,
                    "temperature": temperature,
                    "area": area,
                    "area_acres": acres,
                }
                st.session_state["yield_prediction_error"] = None

            except Exception as e:
                st.session_state["predicted_yield"] = None
                st.session_state["estimated_production"] = None
                st.session_state["yield_prediction_error"] = str(e)
        else:
            # Prevent an old Agriculture prediction from appearing on another page.
            st.session_state.pop("predicted_yield", None)
            st.session_state.pop("estimated_production", None)
            st.session_state.pop("yield_inputs", None)
            st.session_state.pop("yield_prediction_error", None)

    # ------------------------------------------------------------
    # AI YIELD INTELLIGENCE CARD — AGRICULTURE ONLY
    # ------------------------------------------------------------
    if domain_name == "Agriculture" and st.session_state.get("predicted_yield") is not None:
        predicted = float(st.session_state["predicted_yield"])
        estimated_production = float(st.session_state.get("estimated_production", 0.0))
        y_inputs = st.session_state.get("yield_inputs", {})

        st.markdown("---")
        st.markdown("## 🌾 AI Yield Intelligence")
        st.caption(
            "Model-based estimate generated from the selected crop, season, location, rainfall, temperature and land area."
        )

        m1, m2, m3 = st.columns(3)
        m1.metric("🌱 Predicted Yield", f"{predicted:.2f} t/ha")
        m2.metric("📦 Estimated Production", f"{estimated_production:.2f} t")
        m3.metric("📐 Land Area", f"{float(y_inputs.get('area_acres', 0)):.2f} acres")

        with st.expander("🔎 View AI inputs used", expanded=False):
            i1, i2, i3, i4 = st.columns(4)
            i1.metric("Crop", str(y_inputs.get("crop", "—")))
            i2.metric("Season", str(y_inputs.get("crop_type", "—")))
            i3.metric("Rainfall", f"{float(y_inputs.get('rainfall', 0)):.1f} mm")
            i4.metric("Temperature", f"{float(y_inputs.get('temperature', 0)):.1f} °C")

        # A transparent interpretation based only on the model output.
        if predicted < 1:
            outlook = "Lower-yield range"
            guidance = "Review crop suitability, soil inputs, water availability and weather conditions before scaling."
        elif predicted < 3:
            outlook = "Moderate-yield range"
            guidance = "Maintain balanced irrigation and nutrient management and monitor weather conditions."
        else:
            outlook = "Higher-yield range"
            guidance = "Focus on maintaining crop health, timely irrigation and harvest planning."

        st.info(f"📊 Model outlook: **{outlook}**\n\n💡 {guidance}")
        st.caption(
            "⚠️ This is an AI-generated estimate, not a guaranteed harvest outcome. "
            "Actual yield can vary with soil quality, pests, disease, irrigation, farming practices and weather."
        )

    elif domain_name == "Agriculture" and st.session_state.get("yield_prediction_error"):
        st.warning(
            "🌾 Yield prediction could not be generated for the current inputs. "
            "Please check the crop, land area and environmental values and try again."
        )

top3_results = st.session_state.get("br_top3", [])

if top3_results:
            st.divider()

            # STEP 3 is shown only after recommendations have been generated.
            st.markdown("## 3 " + tr_any("Step 3 – Strategic Output"))
            st.caption(
                tr_any(
                    "Select the generated activity you want. Execution, advisory, risks, financial guidance and related schemes will appear below."
                )
            )

            option_labels = [
                f"{i+1}. {tr_any(item['business'])} — {item['score']}/100"
                for i, item in enumerate(top3_results)
            ]

            current = st.session_state.get("br_selected_business")

            default_index = next(
                (
                    i
                    for i, x in enumerate(option_labels)
                    if current and tr_any(current) in x
                ),
                0,
            )

            chosen_label = st.radio(
                "👉 " + tr_any("Select your preferred business option"),
                option_labels,
                index=default_index,
                key="br_option_selector",
            )

            if chosen_label:
                # A language switch re-translates option_labels on this same rerun,
                # so the previously stored radio value may no longer match any entry.
                try:
                    selected_index = option_labels.index(chosen_label)
                except ValueError:
                    selected_index = 0

                selected_business = top3_results[selected_index]["business"]
                st.session_state["br_selected_business"] = selected_business
            selected_cfg = BUSINESS_DOMAIN_CONFIG[domain_name]["businesses"].get(selected_business, {})
            selected_values = apply_location_context_to_business_values(domain_name, values, location)
            selected_score, selected_reasons, selected_gaps = evaluate_business_config(selected_business, selected_values)

            if domain_name == "Agriculture":
                ag_issues, ag_warnings, ag_env = show_agriculture_checks(selected_business, selected_values, location)
                if selected_business in {"Vegetable Cultivation", "Fruit Cultivation"} and ag_issues:
                    st.warning(tr_any("Review the highlighted agriculture checks before treating the plan as ready to scale."))
                if ag_env:
                    st.markdown("#### 🌱 " + tr_any("Environmental crop check"))
                    env_rows = [[tr_data(r.get("crop", "—")), "Pass" if r.get("valid") else "Check", f"{r.get('score','—')}", r.get("reason", "—")] for r in ag_env[:12]]
                    _md_table(["Crop", "Reference check", "Score", "Reason"], env_rows)

            try:
                business_specific_output(selected_business, domain_name, selected_cfg, selected_values, selected_score, selected_reasons, selected_gaps, location)
            except Exception as exc:
                st.error(tr_any("The selected business dashboard encountered an error."))
                st.exception(exc)

# -----------------------------
# FOOTER

# -----------------------------
st.markdown(
    f"""
    <div class="footer">
        {tr("footer")}<br>
        <span class="small-note">{tr("footer_note")}</span>
    </div>
    """,
    unsafe_allow_html=True
)
