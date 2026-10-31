
import json
from pathlib import Path

file_path = Path(__file__).with_name("schemes.json")

new_schemes = [
    ("Atal Pension Yojana (APY)", "Social Security",
     "A contributory pension scheme for eligible subscribers, with pension benefits subject to applicable conditions.",
     "https://www.myscheme.gov.in/"),

    ("Pradhan Mantri Fasal Bima Yojana (PMFBY)", "Agriculture",
     "Crop insurance support for eligible farmers against specified crop losses, subject to policy and seasonal conditions.",
     "https://pmfby.gov.in/"),

    ("Pradhan Mantri Kisan Maan Dhan Yojana (PM-KMY)", "Agriculture",
     "A contributory pension scheme for eligible small and marginal farmers, subject to enrollment requirements.",
     "https://www.myscheme.gov.in/"),

    ("Soil Health Card Scheme", "Agriculture",
     "Provides soil testing information and nutrient recommendations to support informed farming decisions.",
     "https://soilhealth.dac.gov.in/"),

    ("Agriculture Infrastructure Fund (AIF)", "Agriculture",
     "Supports eligible investments in agriculture infrastructure through financing assistance under applicable guidelines.",
     "https://agriinfra.dac.gov.in/"),

    ("PM Vishwakarma", "Business",
     "Provides eligible traditional artisans and craftspeople access to training, toolkit support, credit and market-linkage assistance.",
     "https://pmvishwakarma.gov.in/"),

    ("PM SVANidhi", "Business",
     "A lending initiative supporting eligible street vendors with working-capital credit and related incentives.",
     "https://pmsvanidhi.mohua.gov.in/"),

    ("Prime Minister's Employment Generation Programme (PMEGP)", "Business",
     "Supports eligible entrepreneurs establishing new micro-enterprises through credit-linked assistance.",
     "https://www.kviconline.gov.in/"),

    ("Pradhan Mantri Awas Yojana - Gramin (PMAY-G)", "Housing",
     "Provides housing assistance to eligible rural households under applicable programme guidelines.",
     "https://pmayg.nic.in/"),

    ("Pradhan Mantri Awas Yojana - Urban (PMAY-U)", "Housing",
     "Supports eligible urban households in accessing affordable housing assistance under current programme rules.",
     "https://pmay-urban.gov.in/"),

    ("PM Surya Ghar: Muft Bijli Yojana", "Energy",
     "Supports eligible residential rooftop solar installations under applicable subsidy and application conditions.",
     "https://pmsuryaghar.gov.in/"),

    ("Pradhan Mantri Matru Vandana Yojana (PMMVY)", "Women and Child Welfare",
     "Provides maternity-related financial assistance to eligible pregnant and lactating women, subject to scheme conditions.",
     "https://pmmvy.wcd.gov.in/"),

    ("Janani Suraksha Yojana (JSY)", "Healthcare",
     "A maternal-health programme intended to encourage institutional deliveries among eligible beneficiaries.",
     "https://nhm.gov.in/"),

    ("Pradhan Mantri Jeevan Jyoti Bima Yojana (PMJJBY)", "Social Security",
     "A renewable life insurance scheme for eligible account holders, subject to enrollment and premium requirements.",
     "https://www.jansuraksha.gov.in/"),

    ("Pradhan Mantri Suraksha Bima Yojana (PMSBY)", "Social Security",
     "An accident insurance scheme for eligible account holders, subject to enrollment and policy conditions.",
     "https://www.jansuraksha.gov.in/"),

    ("Pradhan Mantri Shram Yogi Maan-dhan (PM-SYM)", "Social Security",
     "A contributory pension scheme for eligible unorganised-sector workers, subject to age and income requirements.",
     "https://maandhan.in/"),

    ("National Social Assistance Programme (NSAP)", "Social Security",
     "An umbrella programme providing social assistance through different components for eligible vulnerable households.",
     "https://nsap.nic.in/"),

    ("Indira Gandhi National Old Age Pension Scheme (IGNOAPS)", "Social Security",
     "Provides pension assistance to eligible older persons under the National Social Assistance Programme.",
     "https://nsap.nic.in/"),

    ("Indira Gandhi National Widow Pension Scheme (IGNWPS)", "Social Security",
     "Provides pension assistance to eligible widows under the National Social Assistance Programme.",
     "https://nsap.nic.in/"),

    ("Indira Gandhi National Disability Pension Scheme (IGNDPS)", "Social Security",
     "Provides pension assistance to eligible persons with disabilities under the National Social Assistance Programme.",
     "https://nsap.nic.in/")
]

schemes = json.loads(file_path.read_text(encoding="utf-8"))
existing_names = {s["name"] for s in schemes}

added = 0

for name, category, description, url in new_schemes:
    if name in existing_names:
        print("Skipped:", name)
        continue

    schemes.append({
        "name": name,
        "description": description,
        "category": category,
        "official_url": url,
        "rules": {}
    })

    existing_names.add(name)
    added += 1
    print("Added:", name)

file_path.write_text(
    json.dumps(schemes, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8"
)

print("New entries added:", added)
print("Total entries in JSON:", len(schemes))
