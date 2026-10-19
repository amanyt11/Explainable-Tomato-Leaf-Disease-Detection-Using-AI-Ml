"""Agronomic knowledge base and treatment guidelines for tomato leaf conditions."""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class DiseaseProfile:
    """Detailed agronomic and diagnostic profile for a tomato leaf class."""

    class_id: str
    display_name: str
    scientific_name: str
    pathogen_type: str
    severity: str
    color_code: str
    symptoms: List[str]
    immediate_actions: List[str]
    organic_treatment: List[str]
    chemical_treatment: List[str]
    prevention: List[str]


DISEASE_PROFILES: Dict[str, DiseaseProfile] = {
    "Tomato___Bacterial_spot": DiseaseProfile(
        class_id="Tomato___Bacterial_spot",
        display_name="Bacterial Spot",
        scientific_name="Xanthomonas vesicatoria / perforans",
        pathogen_type="Bacterium",
        severity="High",
        color_code="#e67e22",
        symptoms=[
            "Small, dark, water-soaked circular lesions (< 3 mm) on leaves",
            "Lesions develop a distinctive translucent yellow halo",
            "Older spots turn necrotic brown, paper-thin, and may drop out leaving ragged holes",
            "Severe infections cause widespread chlorosis and premature defoliation",
        ],
        immediate_actions=[
            "Isolate infected plants and remove severely blighted foliage during dry weather",
            "Cease overhead sprinkler irrigation immediately to halt splash dispersal",
            "Disinfect pruning shears with 70% isopropyl alcohol between cuts",
        ],
        organic_treatment=[
            "Apply certified organic fixed copper sprays (copper hydroxide or octanoate)",
            "Use bio-fungicide sprays containing Bacillus subtilis or Bacillus amyloliquefaciens",
            "Apply silicon and potassium silicate amendments to strengthen leaf cuticles",
        ],
        chemical_treatment=[
            "Tank-mix copper bactericides with mancozeb to overcome copper-resistant Xanthomonas strains",
            "Apply streptomycin sulfate sprays in transplant seedling stages where registered",
        ],
        prevention=[
            "Use certified pathogen-free seed or hot-water treated seeds (50°C for 25 min)",
            "Implement a minimum 2-year crop rotation away from Solanaceous crops",
            "Use drip irrigation under mulch to keep foliage completely dry",
        ],
    ),
    "Tomato___Early_blight": DiseaseProfile(
        class_id="Tomato___Early_blight",
        display_name="Early Blight",
        scientific_name="Alternaria solani",
        pathogen_type="Fungus",
        severity="Moderate to High",
        color_code="#d35400",
        symptoms=[
            "Dark brown to black necrotic spots with characteristic concentric rings ('target board' pattern)",
            "Lesions typically start on older bottom leaves closest to wet soil",
            "Surrounding leaf tissue turns yellow (chlorotic) as fungal toxins diffuse",
            "Stems may develop dark sunken collar-rot cankers",
        ],
        immediate_actions=[
            "Prune off affected lower leaves up to 30 cm from the ground line",
            "Burn or bag pruned debris; never compost Alternaria-infected foliage",
            "Apply fresh dry straw or plastic mulch beneath the canopy to suppress soil splashing",
        ],
        organic_treatment=[
            "Apply preventive copper octanoate or Bordeaux mixture every 7-10 days",
            "Spray potassium bicarbonate or neem seed oil extracts at early onset",
            "Apply compost tea rich in antagonistic Trichoderma harzianum",
        ],
        chemical_treatment=[
            "Chlorothalonil or azoxystrobin applied preventively before dense canopy closure",
            "Rotate systemic fungicides (e.g., boscalid or difenoconazole) to prevent resistance",
        ],
        prevention=[
            "Ensure wide plant spacing (60-90 cm) for maximum air circulation and rapid leaf drying",
            "Maintain 3-year crop rotation avoiding potatoes, eggplants, and peppers",
            "Stake or cage indeterminate tomato vines off the soil",
        ],
    ),
    "Tomato___Late_blight": DiseaseProfile(
        class_id="Tomato___Late_blight",
        display_name="Late Blight",
        scientific_name="Phytophthora infestans",
        pathogen_type="Oomycete (Water Mold)",
        severity="Severe / Emergency",
        color_code="#c0392b",
        symptoms=[
            "Large, irregular water-soaked pale to greasy green lesions on leaves",
            "Spots rapidly enlarge into dark brown to purplish-black necrotic patches",
            "Delicate white fuzzy fungal mycelium visible on leaf undersides in humid mornings",
            "Canopy rapidly collapses, rots, and emits an odor of decaying vegetation within 48-72 hours",
        ],
        immediate_actions=[
            "Quarantine the field immediately; notify regional agricultural extension",
            "Eradicate and bag severely infected plants in plastic bags under dry conditions",
            "Cease all irrigation and avoid movement through wet vegetation to limit spore spread",
        ],
        organic_treatment=[
            "Heavy preventive copper sulfate / copper hydroxide application prior to cool wet weather",
            "Note: Organic bio-fungicides have limited curative power once Phytophthora enters leaf tissue",
        ],
        chemical_treatment=[
            "Apply systemic oomycete fungicides: cyazofamid, mandipropamid, or fluopicolide",
            "Protectant sprays of chlorothalonil or mancozeb as barrier layers",
        ],
        prevention=[
            "Select resistant cultivars (e.g., 'Defiant PhR', 'Mountain Merit', 'Iron Lady')",
            "Destroy all volunteer tomato and potato plants and cull piles in early spring",
            "Monitor regional late blight forecasting networks (e.g., BlightWatch)",
        ],
    ),
    "Tomato___Leaf_Mold": DiseaseProfile(
        class_id="Tomato___Leaf_Mold",
        display_name="Leaf Mold",
        scientific_name="Passalora fulva (Cladosporium fulvum)",
        pathogen_type="Fungus",
        severity="Moderate",
        color_code="#8e44ad",
        symptoms=[
            "Pale green to yellowish chlorotic spots with indefinite margins on upper leaf surfaces",
            "Olive-green, velvety to brown spore masses develop on corresponding lower leaf undersides",
            "Infected leaves curl, wither, turn golden-brown, and drop prematurely",
            "Predominantly affects greenhouse, high-tunnel, and sheltered humid environments",
        ],
        immediate_actions=[
            "Increase greenhouse ventilation and horizontal airflow immediately to drop relative humidity below 85%",
            "Thin out suckers and crowded leaves to enhance air penetration through the canopy",
            "Prune infected foliage carefully to prevent airborne spore dislodgement",
        ],
        organic_treatment=[
            "Apply bio-fungicides based on Bacillus pumilus or Streptomyces lydicus",
            "Use sulfur or copper fungicides registered for protected greenhouse culture",
        ],
        chemical_treatment=[
            "Apply fungicides such as thiophanate-methyl, cyprodinil + fludioxonil, or azoxystrobin",
            "Alternate FRAC groups to prevent rapid resistance buildup",
        ],
        prevention=[
            "Maintain greenhouse relative humidity consistently below 85% with fans and heating",
            "Grow leaf-mold resistant F1 hybrids containing Cf gene resistance complexes",
            "Sterilize greenhouse structures, stakes, and twine between cropping cycles",
        ],
    ),
    "Tomato___Septoria_leaf_spot": DiseaseProfile(
        class_id="Tomato___Septoria_leaf_spot",
        display_name="Septoria Leaf Spot",
        scientific_name="Septoria lycopersici",
        pathogen_type="Fungus",
        severity="Moderate to High",
        color_code="#b9770e",
        symptoms=[
            "Numerous small circular spots (1.5-3 mm) with dark brown margins and sunken grayish-white centers",
            "Tiny dark pepper-like dots (pycnidia fruiting bodies) visible inside mature spot centers under a lens",
            "Symptoms progress rapidly from bottom leaves upward, causing progressive defoliation",
            "Does not directly infect fruit, but exposed fruit suffers severe sunscald from lost canopy",
        ],
        immediate_actions=[
            "Strip off infected lower foliage and remove from growing area",
            "Clean fallen leaves from under the canopy to minimize overwintering inoculum",
            "Mulch heavily around tomato base to seal soil splash paths",
        ],
        organic_treatment=[
            "Regular preventive sprays of liquid copper octanoate every 7 days",
            "Bacillus subtilis biological fungicides applied during favorable humid conditions",
        ],
        chemical_treatment=[
            "Protectant sprays with chlorothalonil, mancozeb, or polyoxin D",
            "Systemic QoI (pyraclostrobin) or DMI (difenoconazole) fungicides for active spread",
        ],
        prevention=[
            "Minimum 3-year crop rotation away from solanaceous plants and horse-nettle weeds",
            "Stake and trellis vines to maintain foliage at least 45 cm above ground level",
            "Deep fall tillage to bury crop residues and accelerate fungal breakdown",
        ],
    ),
    "Tomato___Spider_mites Two-spotted_spider_mite": DiseaseProfile(
        class_id="Tomato___Spider_mites Two-spotted_spider_mite",
        display_name="Two-Spotted Spider Mite",
        scientific_name="Tetranychus urticae",
        pathogen_type="Arachnid / Acari Pest",
        severity="High (Hot/Dry conditions)",
        color_code="#e74c3c",
        symptoms=[
            "Fine yellow or white stippling (pinpoint chlorotic speckles) on upper leaf surfaces",
            "Delicate silken webbing wrapping leaf tips, petioles, and growing points",
            "Leaves turn bronze, parchment-like, become brittle, and desiccate",
            "Severe infestation leads to total canopy defoliation and plant stunting",
        ],
        immediate_actions=[
            "Dislodge mite colonies and webs with a strong pressurized spray of cold water to leaf undersides",
            "Prune heavily webbed branches and seal them immediately in trash bags",
            "Avoid broad-spectrum synthetic pyrethroid insecticides that destroy beneficial predatory mites",
        ],
        organic_treatment=[
            "Release predatory mites (Phytoseiulus persimilis, Neoseiulus californicus) in greenhouse/canopy",
            "Apply insecticidal soaps or cold-pressed neem oil ensuring thorough coverage of leaf undersides",
            "Spray horticultural summer mineral oil or rosemary/thyme botanical oils",
        ],
        chemical_treatment=[
            "Apply selective miticides: bifenazate, spiromesifen, or abamectin",
            "Rotate modes of action to prevent the notoriously rapid development of acaricide resistance",
        ],
        prevention=[
            "Keep farm roads and surroundings moistened or mulched to suppress dust (dust favors mite outbreaks)",
            "Maintain optimal soil moisture; water-stressed tomato vines attract higher mite populations",
            "Eliminate weed hosts (pigweed, mallow, bindweed) from border rows",
        ],
    ),
    "Tomato___Target_Spot": DiseaseProfile(
        class_id="Tomato___Target_Spot",
        display_name="Target Spot",
        scientific_name="Corynespora cassiicola",
        pathogen_type="Fungus",
        severity="Moderate to High",
        color_code="#995d3f",
        symptoms=[
            "Pinpoint brown lesions with yellow halos on foliage",
            "Lesions expand into round to irregular necrotic spots with light brown centers and faint concentric zoning",
            "Centers of older lesions may crack or tear open",
            "Infects both foliage and developing green/ripe fruit (creating sunken crater-like spots)",
        ],
        immediate_actions=[
            "Improve field drainage and open vine canopy to accelerate drying",
            "Prune lower canopy and dispose of all infected plant tissue away from the field",
            "Avoid overhead watering during morning hours",
        ],
        organic_treatment=[
            "Preventive applications of copper fungicides combined with bio-fungicides",
            "Neem oil and potassium bicarbonate sprays at first detection",
        ],
        chemical_treatment=[
            "Apply fungicides effective against Corynespora: penthiopyrad, fluopyram, or chlorothalonil",
            "Alternate with strobilurins and triazoles according to local resistance guidelines",
        ],
        prevention=[
            "Avoid planting adjacent to other host crops such as cucumber, cotton, or soybean",
            "Maintain balanced nitrogen fertility; excess lush vegetative growth promotes infection",
            "Ensure proper crop residue destruction immediately after final harvest",
        ],
    ),
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": DiseaseProfile(
        class_id="Tomato___Tomato_Yellow_Leaf_Curl_Virus",
        display_name="Tomato Yellow Leaf Curl Virus (TYLCV)",
        scientific_name="Tomato yellow leaf curl begomovirus",
        pathogen_type="Virus (Begomovirus)",
        severity="Severe / Stunting",
        color_code="#f39c12",
        symptoms=[
            "Distinct upward cupping, rolling, and curling of leaf margins ('spooning')",
            "Prominent interveinal chlorosis (yellowing) while veins may remain pale green",
            "Marked reduction in leaflet size, resulting in a stunted 'bonsai' bushy habit",
            "Flower abortion and failure of fruit set; infected young plants yield near zero",
        ],
        immediate_actions=[
            "Rogue out and destroy infected plants immediately upon diagnosis to eliminate viral reservoirs",
            "Control silverleaf whitefly (Bemisia tabaci) populations, the exclusive insect vector",
            "Install 50-mesh insect-proof netting over greenhouse vents and nursery enclosures",
        ],
        organic_treatment=[
            "Deploy bright yellow sticky cards (1 card per 10-20 m²) to trap adult whiteflies",
            "Apply insecticidal soaps, Beauveria bassiana entomopathogenic fungus, or azadirachtin against whiteflies",
            "Release parasitoid wasps (Encarsia formosa or Eretmocerus eremicus)",
        ],
        chemical_treatment=[
            "Viruses cannot be cured with chemical sprays; treatments target whitefly vectors",
            "Systemic neonicotinoids (imidacloprid, thiamethoxam) or flupyradifurone applied at transplanting",
            "Rotate with cyantraniliprole to suppress adult whitefly feeding",
        ],
        prevention=[
            "Plant resistant/tolerant tomato cultivars (e.g., 'Tycoon', 'Charger', 'Grand Slam')",
            "Implement a strict regional tomato-free host period (2-3 months) between seasons",
            "Use UV-reflective silver plastic mulches that repel whiteflies during early growth",
        ],
    ),
    "Tomato___Tomato_mosaic_virus": DiseaseProfile(
        class_id="Tomato___Tomato_mosaic_virus",
        display_name="Tomato Mosaic Virus (ToMV)",
        scientific_name="Tomato mosaic tobamovirus",
        pathogen_type="Virus (Tobamovirus)",
        severity="High (Mechanically Transmitted)",
        color_code="#16a085",
        symptoms=[
            "Alternating light green and dark green mosaic or mottled patterning on leaves",
            "Leaves may become distorted, blistered, wrinkled, or narrow into 'fern-like' or 'shoestring' shapes",
            "Internal browning of fruit wall and uneven ripening",
            "General stunting of the plant canopy and diminished vigor",
        ],
        immediate_actions=[
            "Immediately rogue and incinerate symptomatic plants; do not handle healthy plants after touching",
            "Workers must wash hands and tools thoroughly with 20% non-fat dry milk solution or 10% TSP",
            "Strictly ban tobacco use (cigarettes, chewing tobacco) inside or near tomato greenhouses",
        ],
        organic_treatment=[
            "No chemical cure exists for viral tobamovirus infections",
            "Soak pruning tools in 20% powdered skim milk solution between plants to inactivate viral particles",
            "Apply foliar seaweed extracts to boost innate systemic plant tolerance in mild strains",
        ],
        chemical_treatment=[
            "Direct chemical viricides are ineffective against Tobamoviruses",
            "Sanitize all stakes, trays, benches, and irrigation lines with chlorine dioxide or quaternary ammonium",
        ],
        prevention=[
            "Select ToMV-resistant varieties carrying the Tm-2 or Tm-2^2 resistance gene",
            "Use certified virus-free seed treated with trisodium phosphate (TSP) or dry heat (70°C for 3 days)",
            "Control root-knot nematodes which can facilitate mechanical transmission through root wounds",
        ],
    ),
    "Tomato___healthy": DiseaseProfile(
        class_id="Tomato___healthy",
        display_name="Healthy Tomato Leaf",
        scientific_name="Solanum lycopersicum",
        pathogen_type="Optimal State",
        severity="None",
        color_code="#27ae60",
        symptoms=[
            "Uniform vibrant green coloration with no chlorosis or necrosis",
            "Well-defined serrated margins without curling, cupping, or wilting",
            "Intact surface texture free of lesions, powdery growths, spots, or mite webbing",
            "Healthy vascular venation supporting vigorous photosynthetic activity",
        ],
        immediate_actions=[
            "Continue regular scouting and preventive cultural regimen",
            "Log current canopy condition for longitudinal crop health tracking",
        ],
        organic_treatment=[
            "Maintain soil biological health with organic compost and mycorrhizal inoculants",
            "Apply balanced foliar kelp/micronutrient sprays to sustain vigorous immunity",
        ],
        chemical_treatment=[
            "No chemical treatment required; avoid unnecessary pesticide applications that harm beneficial fauna",
        ],
        prevention=[
            "Adhere to drip irrigation scheduling and keep foliage dry",
            "Maintain optimal soil pH (6.0 - 6.8) and balanced N-P-K nutrition with calcium supplementation to avoid blossom end rot",
            "Ensure adequate ventilation and proper plant spacing",
        ],
    ),
}


def get_disease_profile(class_name: str) -> DiseaseProfile:
    """Retrieve disease profile by class name or return a sensible fallback."""
    if class_name in DISEASE_PROFILES:
        return DISEASE_PROFILES[class_name]
    # Fallback for unknown or alternate class name formatting
    cleaned = class_name.replace(" ", "_")
    for key, profile in DISEASE_PROFILES.items():
        if key.lower() == cleaned.lower() or profile.display_name.lower() in cleaned.lower():
            return profile
    return DiseaseProfile(
        class_id=class_name,
        display_name=class_name.replace("___", " - ").replace("_", " "),
        scientific_name="Solanum lycopersicum condition",
        pathogen_type="General Pathology",
        severity="Informational",
        color_code="#2d7b51",
        symptoms=["Symptom analysis requires manual agricultural extension review."],
        immediate_actions=["Monitor plant daily for changes in leaf color or texture."],
        organic_treatment=["Apply balanced compost tea and maintain dry foliage."],
        chemical_treatment=["Consult local university extension before applying chemical controls."],
        prevention=["Maintain clean tool sanitation, adequate vine spacing, and drip irrigation."],
    )
