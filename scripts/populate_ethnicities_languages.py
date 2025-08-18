"""
Script to populate ethnicities and languages tables with comprehensive data.
This script should be run once after the database tables are created.
"""

import sys
import os
# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sys
import os
# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.system_params.models import db, Ethnicity, Language
import json

# Comprehensive ethnicity data (from the previous hardcoded list)
ETHNICITIES_DATA = [
    # Major ethnic categories
    {"name": "African", "description": "African ethnic group"},
    {"name": "African American", "description": "African American ethnic group"},
    {"name": "Afro-Caribbean", "description": "Afro-Caribbean ethnic group"},
    {"name": "Arab", "description": "Arab ethnic group"},
    {"name": "Asian", "description": "Asian ethnic group"},
    {"name": "Black", "description": "Black ethnic group"},
    {"name": "Caucasian", "description": "Caucasian ethnic group"},
    {"name": "European", "description": "European ethnic group"},
    {"name": "Hispanic or Latino", "description": "Hispanic or Latino ethnic group"},
    {"name": "Indigenous", "description": "Indigenous ethnic group"},
    {"name": "Middle Eastern", "description": "Middle Eastern ethnic group"},
    {"name": "Native American", "description": "Native American ethnic group"},
    {"name": "Pacific Islander", "description": "Pacific Islander ethnic group"},
    {"name": "South Asian", "description": "South Asian ethnic group"},
    {"name": "White", "description": "White ethnic group"},
    {"name": "Other", "description": "Other ethnic group"},
    
    # Specific ethnic groups
    {"name": "Aboriginal", "description": "Aboriginal ethnic group"},
    {"name": "Ainu", "description": "Ainu ethnic group"},
    {"name": "Alaska Native", "description": "Alaska Native ethnic group"},
    {"name": "Amish", "description": "Amish ethnic group"},
    {"name": "Amazigh (Berber)", "description": "Amazigh (Berber) ethnic group"},
    {"name": "Apache", "description": "Apache ethnic group"},
    {"name": "Armenian", "description": "Armenian ethnic group"},
    {"name": "Assyrian", "description": "Assyrian ethnic group"},
    {"name": "Basque", "description": "Basque ethnic group"},
    {"name": "Berber", "description": "Berber ethnic group"},
    {"name": "Boer", "description": "Boer ethnic group"},
    {"name": "Cajun", "description": "Cajun ethnic group"},
    {"name": "Chechen", "description": "Chechen ethnic group"},
    {"name": "Cherokee", "description": "Cherokee ethnic group"},
    {"name": "Chinese", "description": "Chinese ethnic group"},
    {"name": "Circassian", "description": "Circassian ethnic group"},
    {"name": "Coptic", "description": "Coptic ethnic group"},
    {"name": "Cornish", "description": "Cornish ethnic group"},
    {"name": "Cree", "description": "Cree ethnic group"},
    {"name": "Dinka", "description": "Dinka ethnic group"},
    {"name": "Dravidian", "description": "Dravidian ethnic group"},
    {"name": "Dutch", "description": "Dutch ethnic group"},
    {"name": "Eskimo", "description": "Eskimo ethnic group"},
    {"name": "Finnish", "description": "Finnish ethnic group"},
    {"name": "Flemish", "description": "Flemish ethnic group"},
    {"name": "Fula", "description": "Fula ethnic group"},
    {"name": "Gaelic", "description": "Gaelic ethnic group"},
    {"name": "German", "description": "German ethnic group"},
    {"name": "Greek", "description": "Greek ethnic group"},
    {"name": "Han Chinese", "description": "Han Chinese ethnic group"},
    {"name": "Hawaiian", "description": "Hawaiian ethnic group"},
    {"name": "Hmong", "description": "Hmong ethnic group"},
    {"name": "Inuit", "description": "Inuit ethnic group"},
    {"name": "Irish", "description": "Irish ethnic group"},
    {"name": "Italian", "description": "Italian ethnic group"},
    {"name": "Jewish", "description": "Jewish ethnic group"},
    {"name": "Kalenjin", "description": "Kalenjin ethnic group"},
    {"name": "Khoisan", "description": "Khoisan ethnic group"},
    {"name": "Kurdish", "description": "Kurdish ethnic group"},
    {"name": "Ladino", "description": "Ladino ethnic group"},
    {"name": "Latino", "description": "Latino ethnic group"},
    {"name": "Malay", "description": "Malay ethnic group"},
    {"name": "Maori", "description": "Maori ethnic group"},
    {"name": "Mestizo", "description": "Mestizo ethnic group"},
    {"name": "Métis", "description": "Métis ethnic group"},
    {"name": "Mongol", "description": "Mongol ethnic group"},
    {"name": "Navajo", "description": "Navajo ethnic group"},
    {"name": "Ndebele", "description": "Ndebele ethnic group"},
    {"name": "Oromo", "description": "Oromo ethnic group"},
    {"name": "Persian", "description": "Persian ethnic group"},
    {"name": "Punjabi", "description": "Punjabi ethnic group"},
    {"name": "Romani", "description": "Romani ethnic group"},
    {"name": "Sami", "description": "Sami ethnic group"},
    {"name": "Sinhalese", "description": "Sinhalese ethnic group"},
    {"name": "Slavic", "description": "Slavic ethnic group"},
    {"name": "Tamil", "description": "Tamil ethnic group"},
    {"name": "Tatar", "description": "Tatar ethnic group"},
    {"name": "Tibetan", "description": "Tibetan ethnic group"},
    {"name": "Tlingit", "description": "Tlingit ethnic group"},
    {"name": "Ukrainian", "description": "Ukrainian ethnic group"},
    {"name": "Uyghur", "description": "Uyghur ethnic group"},
    {"name": "Vietnamese", "description": "Vietnamese ethnic group"},
    {"name": "Yoruba", "description": "Yoruba ethnic group"},
    {"name": "Zulu", "description": "Zulu ethnic group"},
    
    # Indigenous communities
    {"name": "Abenaki", "description": "Abenaki indigenous community"},
    {"name": "Algonquin", "description": "Algonquin indigenous community"},
    {"name": "Anishinaabe", "description": "Anishinaabe indigenous community"},
    {"name": "Apache", "description": "Apache indigenous community"},
    {"name": "Assiniboine", "description": "Assiniboine indigenous community"},
    {"name": "Atikamekw", "description": "Atikamekw indigenous community"},
    {"name": "Blackfoot", "description": "Blackfoot indigenous community"},
    {"name": "Chippewa", "description": "Chippewa indigenous community"},
    {"name": "Cree", "description": "Cree indigenous community"},
    {"name": "Dakota", "description": "Dakota indigenous community"},
    {"name": "Dene", "description": "Dene indigenous community"},
    {"name": "Haida", "description": "Haida indigenous community"},
    {"name": "Haudenosaunee", "description": "Haudenosaunee indigenous community"},
    {"name": "Innu", "description": "Innu indigenous community"},
    {"name": "Inuit", "description": "Inuit indigenous community"},
    {"name": "Kwakwaka'wakw", "description": "Kwakwaka'wakw indigenous community"},
    {"name": "Lakota", "description": "Lakota indigenous community"},
    {"name": "Lummi", "description": "Lummi indigenous community"},
    {"name": "Mi'kmaq", "description": "Mi'kmaq indigenous community"},
    {"name": "Mohawk", "description": "Mohawk indigenous community"},
    {"name": "Navajo", "description": "Navajo indigenous community"},
    {"name": "Nisga'a", "description": "Nisga'a indigenous community"},
    {"name": "Ojibwe", "description": "Ojibwe indigenous community"},
    {"name": "Seminole", "description": "Seminole indigenous community"},
    {"name": "Tlingit", "description": "Tlingit indigenous community"},
    {"name": "Tsam", "description": "Tsam indigenous community"},
    {"name": "Tsimshian", "description": "Tsimshian indigenous community"},
    {"name": "Zapotec", "description": "Zapotec indigenous community"},
    
    # Additional options
    {"name": "Mixed Ethnicity", "description": "Mixed ethnicity"},
    {"name": "Prefer not to say", "description": "Prefer not to say"}
]

# Comprehensive language data (from the previous hardcoded list)
LANGUAGES_DATA = [
    {"name": "Abkhaz", "iso_code": "ab"},
    {"name": "Afar", "iso_code": "aa"},
    {"name": "Afrikaans", "iso_code": "af"},
    {"name": "Akan", "iso_code": "ak"},
    {"name": "Albanian", "iso_code": "sq"},
    {"name": "Amharic", "iso_code": "am"},
    {"name": "Arabic", "iso_code": "ar"},
    {"name": "Aragonese", "iso_code": "an"},
    {"name": "Armenian", "iso_code": "hy"},
    {"name": "Assamese", "iso_code": "as"},
    {"name": "Avaric", "iso_code": "av"},
    {"name": "Avestan", "iso_code": "ae"},
    {"name": "Aymara", "iso_code": "ay"},
    {"name": "Azerbaijani", "iso_code": "az"},
    {"name": "Bambara", "iso_code": "bm"},
    {"name": "Bashkir", "iso_code": "ba"},
    {"name": "Basque", "iso_code": "eu"},
    {"name": "Belarusian", "iso_code": "be"},
    {"name": "Bengali", "iso_code": "bn"},
    {"name": "Bihari", "iso_code": "bh"},
    {"name": "Bislama", "iso_code": "bi"},
    {"name": "Bosnian", "iso_code": "bs"},
    {"name": "Breton", "iso_code": "br"},
    {"name": "Bulgarian", "iso_code": "bg"},
    {"name": "Burmese", "iso_code": "my"},
    {"name": "Catalan", "iso_code": "ca"},
    {"name": "Chamorro", "iso_code": "ch"},
    {"name": "Chechen", "iso_code": "ce"},
    {"name": "Chichewa", "iso_code": "ny"},
    {"name": "Chinese", "iso_code": "zh"},
    {"name": "Chuvash", "iso_code": "cv"},
    {"name": "Cornish", "iso_code": "kw"},
    {"name": "Corsican", "iso_code": "co"},
    {"name": "Cree", "iso_code": "cr"},
    {"name": "Croatian", "iso_code": "hr"},
    {"name": "Czech", "iso_code": "cs"},
    {"name": "Danish", "iso_code": "da"},
    {"name": "Divehi", "iso_code": "dv"},
    {"name": "Dutch", "iso_code": "nl"},
    {"name": "Dzongkha", "iso_code": "dz"},
    {"name": "English", "iso_code": "en"},
    {"name": "Esperanto", "iso_code": "eo"},
    {"name": "Estonian", "iso_code": "et"},
    {"name": "Ewe", "iso_code": "ee"},
    {"name": "Faroese", "iso_code": "fo"},
    {"name": "Fijian", "iso_code": "fj"},
    {"name": "Finnish", "iso_code": "fi"},
    {"name": "French", "iso_code": "fr"},
    {"name": "Fula", "iso_code": "ff"},
    {"name": "Galician", "iso_code": "gl"},
    {"name": "Georgian", "iso_code": "ka"},
    {"name": "German", "iso_code": "de"},
    {"name": "Greek", "iso_code": "el"},
    {"name": "Guaraní", "iso_code": "gn"},
    {"name": "Gujarati", "iso_code": "gu"},
    {"name": "Haitian", "iso_code": "ht"},
    {"name": "Hausa", "iso_code": "ha"},
    {"name": "Hebrew", "iso_code": "he"},
    {"name": "Herero", "iso_code": "hz"},
    {"name": "Hindi", "iso_code": "hi"},
    {"name": "Hiri Motu", "iso_code": "ho"},
    {"name": "Hungarian", "iso_code": "hu"},
    {"name": "Interlingua", "iso_code": "ia"},
    {"name": "Indonesian", "iso_code": "id"},
    {"name": "Interlingue", "iso_code": "ie"},
    {"name": "Irish", "iso_code": "ga"},
    {"name": "Igbo", "iso_code": "ig"},
    {"name": "Inupiaq", "iso_code": "ik"},
    {"name": "Ido", "iso_code": "io"},
    {"name": "Icelandic", "iso_code": "is"},
    {"name": "Italian", "iso_code": "it"},
    {"name": "Inuktitut", "iso_code": "iu"},
    {"name": "Japanese", "iso_code": "ja"},
    {"name": "Javanese", "iso_code": "jv"},
    {"name": "Kalaallisut", "iso_code": "kl"},
    {"name": "Kannada", "iso_code": "kn"},
    {"name": "Kanuri", "iso_code": "kr"},
    {"name": "Kashmiri", "iso_code": "ks"},
    {"name": "Kazakh", "iso_code": "kk"},
    {"name": "Khmer", "iso_code": "km"},
    {"name": "Kikuyu", "iso_code": "ki"},
    {"name": "Kinyarwanda", "iso_code": "rw"},
    {"name": "Kirundi", "iso_code": "rn"},
    {"name": "Komi", "iso_code": "kv"},
    {"name": "Kongo", "iso_code": "kg"},
    {"name": "Korean", "iso_code": "ko"},
    {"name": "Kurdish", "iso_code": "ku"},
    {"name": "Kwanyama", "iso_code": "kj"},
    {"name": "Kyrgyz", "iso_code": "ky"},
    {"name": "Latin", "iso_code": "la"},
    {"name": "Luxembourgish", "iso_code": "lb"},
    {"name": "Luganda", "iso_code": "lg"},
    {"name": "Limburgish", "iso_code": "li"},
    {"name": "Lingala", "iso_code": "ln"},
    {"name": "Lao", "iso_code": "lo"},
    {"name": "Lithuanian", "iso_code": "lt"},
    {"name": "Luba-Katanga", "iso_code": "lu"},
    {"name": "Latvian", "iso_code": "lv"},
    {"name": "Manx", "iso_code": "gv"},
    {"name": "Macedonian", "iso_code": "mk"},
    {"name": "Malayalam", "iso_code": "ml"},
    {"name": "Malagasy", "iso_code": "mg"},
    {"name": "Maltese", "iso_code": "mt"},
    {"name": "Maori", "iso_code": "mi"},
    {"name": "Marathi", "iso_code": "mr"},
    {"name": "Marshallese", "iso_code": "mh"},
    {"name": "Mongolian", "iso_code": "mn"},
    {"name": "Nauru", "iso_code": "na"},
    {"name": "Navajo", "iso_code": "nv"},
    {"name": "North Ndebele", "iso_code": "nd"},
    {"name": "Nepali", "iso_code": "ne"},
    {"name": "Ndonga", "iso_code": "ng"},
    {"name": "Norwegian Bokmål", "iso_code": "nb"},
    {"name": "Norwegian Nynorsk", "iso_code": "nn"},
    {"name": "Norwegian", "iso_code": "no"},
    {"name": "Nuosu", "iso_code": "ii"},
    {"name": "Southern Ndebele", "iso_code": "nr"},
    {"name": "Occitan", "iso_code": "oc"},
    {"name": "Ojibwe", "iso_code": "oj"},
    {"name": "Old Church Slavonic", "iso_code": "cu"},
    {"name": "Oromo", "iso_code": "om"},
    {"name": "Oriya", "iso_code": "or"},
    {"name": "Ossetian", "iso_code": "os"},
    {"name": "Panjabi", "iso_code": "pa"},
    {"name": "Pāli", "iso_code": "pi"},
    {"name": "Persian", "iso_code": "fa"},
    {"name": "Polish", "iso_code": "pl"},
    {"name": "Pashto", "iso_code": "ps"},
    {"name": "Portuguese", "iso_code": "pt"},
    {"name": "Quechua", "iso_code": "qu"},
    {"name": "Romansh", "iso_code": "rm"},
    {"name": "Kirundi", "iso_code": "rn"},
    {"name": "Romanian", "iso_code": "ro"},
    {"name": "Russian", "iso_code": "ru"},
    {"name": "Sanskrit", "iso_code": "sa"},
    {"name": "Sardinian", "iso_code": "sc"},
    {"name": "Sindhi", "iso_code": "sd"},
    {"name": "Northern Sami", "iso_code": "se"},
    {"name": "Samoan", "iso_code": "sm"},
    {"name": "Sango", "iso_code": "sg"},
    {"name": "Serbian", "iso_code": "sr"},
    {"name": "Scottish Gaelic", "iso_code": "gd"},
    {"name": "Shona", "iso_code": "sn"},
    {"name": "Sinhala", "iso_code": "si"},
    {"name": "Slovak", "iso_code": "sk"},
    {"name": "Slovene", "iso_code": "sl"},
    {"name": "Somali", "iso_code": "so"},
    {"name": "Southern Sotho", "iso_code": "st"},
    {"name": "Spanish", "iso_code": "es"},
    {"name": "Sundanese", "iso_code": "su"},
    {"name": "Swahili", "iso_code": "sw"},
    {"name": "Swati", "iso_code": "ss"},
    {"name": "Swedish", "iso_code": "sv"},
    {"name": "Tamil", "iso_code": "ta"},
    {"name": "Telugu", "iso_code": "te"},
    {"name": "Tajik", "iso_code": "tg"},
    {"name": "Thai", "iso_code": "th"},
    {"name": "Tigrinya", "iso_code": "ti"},
    {"name": "Tibetan", "iso_code": "bo"},
    {"name": "Turkmen", "iso_code": "tk"},
    {"name": "Tagalog", "iso_code": "tl"},
    {"name": "Tswana", "iso_code": "tn"},
    {"name": "Tonga", "iso_code": "to"},
    {"name": "Turkish", "iso_code": "tr"},
    {"name": "Tsonga", "iso_code": "ts"},
    {"name": "Tatar", "iso_code": "tt"},
    {"name": "Twi", "iso_code": "tw"},
    {"name": "Tahitian", "iso_code": "ty"},
    {"name": "Uyghur", "iso_code": "ug"},
    {"name": "Ukrainian", "iso_code": "uk"},
    {"name": "Urdu", "iso_code": "ur"},
    {"name": "Uzbek", "iso_code": "uz"},
    {"name": "Venda", "iso_code": "ve"},
    {"name": "Vietnamese", "iso_code": "vi"},
    {"name": "Volapük", "iso_code": "vo"},
    {"name": "Walloon", "iso_code": "wa"},
    {"name": "Welsh", "iso_code": "cy"},
    {"name": "Wolof", "iso_code": "wo"},
    {"name": "Western Frisian", "iso_code": "fy"},
    {"name": "Xhosa", "iso_code": "xh"},
    {"name": "Yiddish", "iso_code": "yi"},
    {"name": "Yoruba", "iso_code": "yo"},
    {"name": "Zhuang", "iso_code": "za"},
    {"name": "Chinese", "iso_code": "zh"},
    {"name": "Zulu", "iso_code": "zu"}
]

def populate_ethnicities():
    """Populate the ethnicities table with data."""
    print("Populating ethnicities...")
    for ethnicity_data in ETHNICITIES_DATA:
        # Check if ethnicity already exists
        existing = Ethnicity.query.filter_by(name=ethnicity_data['name']).first()
        if not existing:
            ethnicity = Ethnicity(**ethnicity_data)
            db.session.add(ethnicity)
            print(f"Added ethnicity: {ethnicity_data['name']}")
    
    db.session.commit()
    print("Ethnicities populated successfully.")

def populate_languages():
    """Populate the languages table with data."""
    print("Populating languages...")
    for language_data in LANGUAGES_DATA:
        # Check if language already exists
        existing = Language.query.filter_by(name=language_data['name']).first()
        if not existing:
            language = Language(**language_data)
            db.session.add(language)
            print(f"Added language: {language_data['name']}")
    
    db.session.commit()
    print("Languages populated successfully.")

def main():
    """Main function to run the population script."""
    app = create_app()
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Populate data
        populate_ethnicities()
        populate_languages()
        
        print("Database population completed!")

if __name__ == '__main__':
    main()