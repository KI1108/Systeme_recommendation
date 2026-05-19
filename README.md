Creation de la base de données
Pour la bd utilisons supabase
les tables dont a besoin

utilisateurs
formations
bourse
recommendation

## Creation des tables


--Table utilisateurs
CREATE TABLE utilisateurs(
  id SERIAL PRIMARY KEY,
  nom VARCHAR(100) NOT NULL,
  prenom VARCHAR(100) NOT NULL,
  email VARCHAR(200) UNIQUE NOT NULL,
  age INTEGER,
  pays VARCHAR(100) NOT NULL,
  niveau_etude VARCHAR(50) NOT NULL,
  domaine VARCHAR(100) NOT NULL,
  objectif VARCHAR(100),
  langue VARCHAR(50) DEFAULT 'Francais',
  created_at TIMESTAMP DEFAULT NOW()
);

--Table formations
CREATE TABLE formations(
  id SERIAL PRIMARY KEY,
  titre VARCHAR(300) NOT NULL,
  descriptions TEXT,
  domaine VARCHAR(100) NOT NULL,
  niveau_requis VARCHAR(100) NOT NULL,
  pays_disponible VARCHAR(100) DEFAULT 'international',
  langue VARCHAR(50) DEFAULT 'français',
  duree VARCHAR(100),
  est_gratuit BOOLEAN DEFAULT FALSE,
  lien VARCHAR(500),
  organisme VARCHAR(200),
  created_at TIMESTAMP DEFAULT NOW()
);

--Table bourses
CREATE TABLE bourses(
  id SERIAL PRIMARY KEY,
  titre VARCHAR(300) NOT NULL,
  organisme VARCHAR(200) NOT NULL,
  descriptions TEXT,
  pays_eligible VARCHAR(200) DEFAULT 'tous',
  niveau_requis VARCHAR(50) NOT NULL,
  domaine VARCHAR(100) NOT NULL,
  montant VARCHAR(200),
  date_limite DATE,
  type_bourse VARCHAR(100),
  lien VARCHAR(500),
  created_at TIMESTAMP DEFAULT NOW()
);

--table recommendations

CREATE TABLE recommendations(
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES utilisateurs(id) ON DELETE CASCADE,
  item_id INTEGER NOT NULL,
  type_item VARCHAR(20) NOT NULL,
  score INTEGER NOT NULL,
  raisons TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

## creation et activation environnement virtuel 
python -m venv env
env\Scripts\activate

<!-- Insertion data -->

INSERT INTO formations
    (titre, descriptions, domaine, niveau_requis, pays_disponible, langue, duree, est_gratuit, lien, organisme)

VALUES
--formation 1
(
'Introduction à python et Data Science',
'Apprenez les bases de python et de l\'analyse de données avec des projets concret.
Idéal pour débuter en data science',
'Informatique','lycée',
'international','français','8 semaines', TRUE,
'https://www.coursera.org', 'Coursera / IBM'
)
INSERT INTO formations (titre, descriptions, domaine, niveau_requis, pays_disponible, langue, duree, est_gratuit, lien, organisme, created_at) VALUES

('Développement Web Full Stack',
'Formation complète couvrant HTML, CSS, JavaScript, React et Node.js. Apprenez à concevoir et déployer des applications web modernes de A à Z.',
'Informatique', 'Baccalauréat', 'International', 'Français', '6 mois', FALSE,
'https://www.openclassrooms.com/fr/paths/185-developpeur-web',
'OpenClassrooms', '2024-01-10 09:00:00'),

('Analyse Financière et Gestion de Portefeuille',
'Maîtrisez les outils d''analyse financière, la lecture des états financiers et la gestion d''actifs pour évoluer dans le secteur bancaire et financier.',
'Finance', 'Licence', 'International', 'Français', '4 mois', FALSE,
'https://www.coursera.org/specializations/financial-analysis',
'Coursera / HEC Paris', '2024-01-20 10:30:00'),

('Marketing Digital et Réseaux Sociaux',
'Découvrez les stratégies de marketing en ligne, la gestion des réseaux sociaux, le SEO et la publicité digitale pour booster la visibilité de votre entreprise.',
'Marketing', 'BTS', 'International', 'Français', '3 mois', TRUE,
'https://learndigital.withgoogle.com/ateliersnumeriques',
'Google Ateliers Numériques', '2024-02-05 08:00:00'),

('Introduction à l''Électronique Embarquée',
'Formation pratique sur les microcontrôleurs, Arduino et Raspberry Pi. Idéale pour concevoir des systèmes électroniques intelligents.',
'Électronique', 'Baccalauréat', 'International', 'Français', '2 mois', TRUE,
'https://www.fun-mooc.fr/fr/cours/electronique-embarquee',
'FUN-MOOC / Université de Bordeaux', '2024-02-18 14:00:00'),

('Santé Publique et Épidémiologie',
'Explorez les fondements de la santé publique, la surveillance épidémiologique et la gestion des crises sanitaires à l''échelle nationale et internationale.',
'Médecine', 'Master', 'International', 'Français', '5 mois', FALSE,
'https://www.coursera.org/learn/epidemiology',
'Coursera / Johns Hopkins University', '2024-03-01 11:00:00'),

('Droit des Affaires et Contrats Commerciaux',
'Apprenez les bases du droit commercial, la rédaction de contrats, la gestion des litiges et la conformité juridique pour les entreprises en Afrique francophone.',
'Droit', 'Licence', 'Afrique Francophone', 'Français', '3 mois', FALSE,
'https://www.ohada.com/formations',
'OHADA / ERSUMA', '2024-03-15 09:30:00'),

('Gestion des Ressources Humaines Modernes',
'Formation axée sur le recrutement, la gestion des talents, la paie, la législation du travail et le management d''équipe dans un contexte africain.',
'Ressources Humaines', 'Licence', 'Afrique Francophone', 'Français', '3 mois', FALSE,
'https://www.africamanagementinitiative.org/formations',
'Africa Management Initiative (AMI)', '2024-04-02 10:00:00'),

('Comptabilité Générale et Logiciels de Gestion',
'Maîtrisez le plan comptable OHADA, la saisie comptable, les déclarations fiscales et l''utilisation de logiciels comme Sage et QuickBooks.',
'Comptabilité', 'BTS', 'Afrique Francophone', 'Français', '4 mois', FALSE,
'https://www.groupeiscbf.com/formations-comptabilite',
'Institut Supérieur de Commerce de Ouagadougou', '2024-04-20 08:30:00'),

('Gestion de Projets de Construction',
'Formez-vous aux techniques de planification, d''estimation des coûts, de suivi de chantier et de gestion des équipes dans le secteur du BTP.',
'Génie Civil', 'Licence', 'International', 'Français', '5 mois', FALSE,
'https://www.pmibf.org/formations-genie-civil',
'PMI Burkina Faso / École Polytechnique', '2024-05-08 13:00:00');



INSERT INTO bourses
(titre, descriptions, organisme, pays_eligible, niveau_requis, domaine, montant, type_bourse, lien)
VALUES
(
'Bourse Excellence AFD-Master en France',
'Financement complet pour etudier en France.
Couvre frais de scolarité, billet avion et vie.',
'Agence Française de Developpement',
'tous',
'licence',
'informatique',
'Frais de scolarité + 850 euro/mois',
'excellence',
'https://www.afd.fr'
);
INSERT INTO bourses (titre, organisme, descriptions, pays_eligible, niveau_requis, domaine, montant, date_limite, type_bourse, lien, created_at) VALUES

('Bourse d''Excellence AFD Afrique Francophone',
'Agence Française de Développement (AFD)',
'Bourse destinée aux étudiants africains francophones souhaitant poursuivre un Master en France dans les domaines du développement durable et de l''informatique. Couvre les frais de scolarité, le logement et une allocation mensuelle.',
'Burkina Faso, Mali, Sénégal, Côte d''Ivoire, Guinée',
'Licence', 'Informatique',
'15 000 € / an (scolarité + logement + allocation 800€/mois)',
'2024-03-31',
'Bourse complète',
'https://www.afd.fr/fr/bourses-excellence',
'2024-01-05 08:00:00'),

('Bourse Mastercard Foundation - Université de Dakar',
'Mastercard Foundation',
'Programme de bourses pour jeunes talents africains issus de milieux défavorisés. Couvre intégralement les études de Master en Finance et Commerce à l''Université de Dakar.',
'Burkina Faso, Mali, Sénégal, Côte d''Ivoire, Guinée, Niger, Togo, Bénin',
'Licence', 'Finance',
'Prise en charge complète (scolarité, logement, alimentation, transport)',
'2024-04-15',
'Bourse complète',
'https://mastercardfdn.org/scholarships',
'2024-01-12 09:30:00'),

('Bourse Google Generation Scholarship',
'Google Africa',
'Bourse pour étudiants africains passionnés par le numérique et le marketing digital. Inclut un accès aux formations Google, un mentorat et une allocation financière.',
'Tous les pays africains',
'BTS', 'Marketing',
'5 000 USD + accès aux certifications Google',
'2024-05-01',
'Bourse partielle',
'https://buildyourfuture.withgoogle.com/scholarships/generation-google-scholarship-apac',
'2024-01-20 10:00:00'),

('Bourse Orange Ventures Tech Africa',
'Groupe Orange / Orange Ventures',
'Programme de financement dédié aux étudiants et jeunes ingénieurs africains en électronique et télécommunications. Comprend un stage rémunéré au sein du groupe Orange.',
'Burkina Faso, Mali, Sénégal, Côte d''Ivoire, Cameroun',
'BTS', 'Électronique',
'3 000 000 FCFA / an + stage rémunéré',
'2024-04-30',
'Bourse partielle',
'https://www.orange.com/fr/bourses-tech-africa',
'2024-02-01 11:00:00'),

('Bourse OMS / ONG Santé Sans Frontières',
'Organisation Mondiale de la Santé (OMS)',
'Financement de thèses et de spécialisations en santé publique et épidémiologie pour les professionnels de santé africains. Stage pratique dans un bureau régional OMS inclus.',
'Tous pays membres de l''OMS en Afrique subsaharienne',
'Master', 'Médecine',
'20 000 USD / an + indemnités de stage',
'2024-06-30',
'Bourse de recherche',
'https://www.who.int/scholarships',
'2024-02-10 09:00:00'),

('Bourse OHADA Droit des Affaires',
'Organisation pour l''Harmonisation en Afrique du Droit des Affaires',
'Bourse pour étudiants en droit souhaitant se spécialiser dans le droit des affaires africain. Formation à l''ERSUMA (Porto-Novo) avec certification officielle OHADA.',
'Tous pays membres de l''OHADA',
'Licence', 'Droit',
'2 500 000 FCFA (scolarité + hébergement)',
'2024-05-15',
'Bourse complète',
'https://www.ohada.com/bourses-ersuma',
'2024-02-18 14:00:00'),

('Bourse AMI Leadership & RH Afrique',
'Africa Management Initiative (AMI)',
'Programme de développement du leadership pour les professionnels RH africains. Formation en ligne + présentiel dans les capitales africaines partenaires.',
'Burkina Faso, Kenya, Ghana, Rwanda, Côte d''Ivoire, Sénégal',
'Licence', 'Ressources Humaines',
'4 500 USD (formation complète + matériel)',
'2024-07-01',
'Bourse de formation',
'https://www.africamanagementinitiative.org/bourses',
'2024-03-01 08:30:00'),

('Bourse UEMOA Comptabilité et Gestion',
'Union Économique et Monétaire Ouest-Africaine (UEMOA)',
'Bourse régionale pour les étudiants en comptabilité et finances publiques des pays membres de l''UEMOA. Priorité aux candidats souhaitant intégrer les institutions publiques.',
'Burkina Faso, Mali, Sénégal, Côte d''Ivoire, Niger, Togo, Bénin, Guinée-Bissau',
'BTS', 'Comptabilité',
'1 800 000 FCFA / an',
'2024-06-15',
'Bourse régionale',
'https://www.uemoa.int/fr/bourses-comptabilite',
'2024-03-10 10:00:00'),

('Bourse BAD Infrastructure et Génie Civil',
'Banque Africaine de Développement (BAD)',
'Programme de bourses pour ingénieurs et techniciens en génie civil afin de renforcer les capacités africaines en matière d''infrastructures. Inclut un contrat de stage à la BAD.',
'Tous pays membres de la BAD',
'Licence', 'Génie Civil',
'25 000 USD / an + indemnités de stage BAD',
'2024-08-31',
'Bourse de recherche',
'https://www.afdb.org/fr/bourses-infrastructure',
'2024-03-20 11:00:00');


INSERT INTO recommendations (user_id, item_id, type_item, score, raisons, created_at) VALUES

-- Aminata (id=1) | Informatique | Licence | Burkina Faso
(1, 1, 'formation', 95,
'Correspond exactement au domaine Informatique d''Aminata. Niveau Baccalauréat requis compatible avec sa Licence. Formation Full Stack très demandée sur le marché burkinabè.',
'2024-01-16 09:00:00'),

-- Aminata (id=1) | Informatique | Licence | Burkina Faso → Bourse AFD
(1, 1, 'bourse', 92,
'La bourse AFD cible explicitement le Burkina Faso et le domaine Informatique. Niveau Licence d''Aminata correspond parfaitement au niveau requis. Objectif : trouver un emploi facilité par ce financement.',
'2024-01-16 09:05:00'),

-- Moussa (id=2) | Finance | Master | Mali
(2, 2, 'formation', 97,
'Formation en Analyse Financière parfaitement alignée avec le domaine Finance de Moussa. Niveau Master requis correspond à son profil. Objectif de changement de carrière bien supporté par HEC Paris.',
'2024-02-04 10:00:00'),

-- Moussa (id=2) | Finance | Master | Mali → Bourse Mastercard
(2, 2, 'bourse', 90,
'La bourse Mastercard Foundation cible le Mali et le domaine Finance. Moussa est issu d''un pays éligible et son niveau Licence satisfait les conditions. Bourse complète idéale pour changer de carrière.',
'2024-02-04 10:10:00'),

-- Fatou (id=3) | Marketing | BTS | Côte d'Ivoire
(3, 3, 'formation', 94,
'Formation Marketing Digital de Google parfaitement adaptée au profil BTS de Fatou en Marketing. Formation gratuite accessible depuis la Côte d''Ivoire. Objectif montée en compétences bien couvert.',
'2024-02-19 14:00:00'),

-- Fatou (id=3) | Marketing | BTS | Côte d'Ivoire → Bourse Google
(3, 3, 'bourse', 88,
'Bourse Google Generation Scholarship ouverte à toute l''Afrique, domaine Marketing, niveau BTS requis. Inclut certifications Google très valorisées pour l''objectif de Fatou.',
'2024-02-19 14:10:00'),

-- Ibrahim (id=4) | Électronique | Baccalauréat | Guinée
(4, 4, 'formation', 96,
'Formation Électronique Embarquée gratuite parfaitement adaptée au profil Baccalauréat d''Ibrahim en Électronique. Disponible en ligne depuis la Guinée. Objectif certification directement atteignable.',
'2024-03-06 09:00:00'),

-- Ibrahim (id=4) | Électronique | Baccalauréat | Guinée → Bourse Orange
(4, 4, 'bourse', 85,
'Bourse Orange Ventures couvre l''Électronique et inclut un stage rémunéré. Niveau BTS requis proche du Baccalauréat d''Ibrahim. Bonne opportunité pour atteindre son objectif de certification.',
'2024-03-06 09:10:00'),

-- Marie (id=5) | Médecine | Doctorat | Burkina Faso
(5, 5, 'formation', 98,
'Formation Santé Publique et Épidémiologie de Johns Hopkins parfaitement alignée avec le Doctorat en Médecine de Marie. Niveau Master requis largement satisfait. Objectif spécialisation directement adressé.',
'2024-03-21 11:00:00'),

-- Marie (id=5) | Médecine | Doctorat | Burkina Faso → Bourse OMS
(5, 5, 'bourse', 99,
'Bourse OMS dédiée à la Médecine et Santé Publique, niveau Master requis compatible avec le Doctorat de Marie. Burkina Faso pays éligible. Score maximal car correspond à 100% à son objectif de spécialisation.',
'2024-03-21 11:10:00');

INSERT INTO utilisateurs (nom, prenom, email, age, pays, niveau_etude, domaine, objectif, langue, created_at) VALUES
('Ouédraogo', 'Aminata', 'aminata.ouedraogo@gmail.com', 24, 'Burkina Faso', 'Licence', 'Informatique', 'Trouver un emploi', 'Français', '2024-01-15 08:30:00'),
('Traoré', 'Moussa', 'moussa.traore@yahoo.fr', 31, 'Mali', 'Master', 'Finance', 'Changer de carrière', 'Français', '2024-02-03 10:15:00'),
('Koné', 'Fatou', 'fatou.kone@outlook.com', 27, 'Côte d''Ivoire', 'BTS', 'Marketing', 'Monter en compétences', 'Français', '2024-02-18 14:45:00'),
('Diallo', 'Ibrahim', 'ibrahim.diallo@gmail.com', 22, 'Guinée', 'Baccalauréat', 'Électronique', 'Obtenir une certification', 'Français', '2024-03-05 09:00:00'),
('Sawadogo', 'Marie', 'marie.sawadogo@gmail.com', 35, 'Burkina Faso', 'Doctorat', 'Médecine', 'Se spécialiser', 'Français', '2024-03-20 11:30:00'),
('Coulibaly', 'Seydou', 'seydou.coulibaly@yahoo.fr', 29, 'Mali', 'Licence', 'Droit', 'Trouver un emploi', 'Français', '2024-04-02 16:00:00'),
('Bamba', 'Aïssata', 'aissata.bamba@gmail.com', 26, 'Côte d''Ivoire', 'Master', 'Ressources Humaines', 'Créer une entreprise', 'Français', '2024-04-17 08:00:00'),
('Compaoré', 'Luc', 'luc.compaore@hotmail.com', 33, 'Burkina Faso', 'BTS', 'Comptabilité', 'Monter en compétences', 'Français', '2024-05-10 13:20:00'),
('Sylla', 'Kadiatou', 'kadiatou.sylla@gmail.com', 21, 'Sénégal', 'Baccalauréat', 'Commerce', 'Obtenir une certification', 'Français', '2024-05-25 07:45:00'),
('Zongo', 'Pascal', 'pascal.zongo@gmail.com', 38, 'Burkina Faso', 'Licence', 'Génie Civil', 'Se spécialiser', 'Français', '2024-06-08 15:10:00');