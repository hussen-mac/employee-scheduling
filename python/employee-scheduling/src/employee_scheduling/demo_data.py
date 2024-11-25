from datetime import date, datetime, time, timedelta
from itertools import product
from enum import Enum
from random import Random
from typing import Generator, List
from dataclasses import dataclass, field
from datetime import date

from .domain import *
import pandas as pd
import os


def extract_predictions(file_path: str, period: str) -> dict:
    """
    Extrait les prédictions à partir d'un fichier CSV et les structure
    dans un dictionnaire basé sur une période spécifique.

    :param file_path: Chemin du fichier CSV contenant les prévisions.
    :param period: Période associée aux prévisions.
    :return: Un dictionnaire contenant les prévisions pour la période donnée.
    """
    df = pd.read_csv(file_path, sep=",")
    last_14 = df.tail(14)
    predictions = [{"date": row["ds"], "value": int(row["yhat"])} for _, row in last_14.iterrows()]
    return {period: predictions}

all_predictions = {}

csv_files = {
    "6h-14h": "forecast.csv",
    "14h-23h": "forecast_1.csv",
    "23h-5h": "forecast_2.csv",
}


csv_directory = os.path.abspath(
    os.path.join(os.getcwd(), '..', 'prevision', 'prediction_train')
)

for period, file_name in csv_files.items():
    file_path = os.path.join(csv_directory, file_name)
    if os.path.exists(file_path):
        all_predictions.update(extract_predictions(file_path, period))
    else:
        print(f"Le fichier {file_name} n'existe pas dans le répertoire spécifié.")


class DemoData(Enum):
    SMALL = 'SMALL'
    LARGE = 'LARGE'


@dataclass(frozen=True, kw_only=True)
class CountDistribution:
    count: int
    weight: float


def counts(distributions: tuple) -> tuple[int, ...]:
    """
    Extrait les comptes des distributions.

    :param distributions: Tuple contenant des objets `CountDistribution`.
    :return: Tuple des comptes extraits.
    """
    return tuple(distribution.count for distribution in distributions)


def weights(distributions: tuple) -> tuple[float, ...]:
    """
    Extrait les poids des distributions.

    :param distributions: Tuple contenant des objets `CountDistribution`.
    :return: Tuple des poids extraits.
    """
    return tuple(distribution.weight for distribution in distributions)


@dataclass(kw_only=True)
class DemoDataParameters:
    locations: tuple[str, ...]
    required_skills: tuple[str, ...] 
    optional_skills: tuple[str, ...]
    days_in_schedule: int
    employee_count: int
    optional_skill_distribution: tuple[CountDistribution, ...]
    shift_count_distribution: tuple[CountDistribution, ...]
    availability_count_distribution: tuple[CountDistribution, ...]
    random_seed: int = field(default=37)


demo_data_to_parameters: dict[DemoData, DemoDataParameters] = {
    DemoData.SMALL: DemoDataParameters(
        locations=("affaire", "première_classe", "mono_space", "confort"),
        required_skills= ("conduite"),
        optional_skills=("Beginner", "Intermediate", "Expert"),
        days_in_schedule=14,
        employee_count=47,
        optional_skill_distribution=(
            CountDistribution(count=1, weight=3),
            CountDistribution(count=2, weight=1)
        ),
        shift_count_distribution=(
            CountDistribution(count=1, weight=0.9),
            CountDistribution(count=2, weight=0.1)
        ),
        availability_count_distribution=(
            CountDistribution(count=1, weight=4),
            CountDistribution(count=2, weight=3),
            CountDistribution(count=3, weight=2),
            CountDistribution(count=4, weight=1)
        ),
        random_seed=37
    ),

    DemoData.LARGE: DemoDataParameters(
        locations=("affaire", "première_classe", "mono_space", "confort"),
        required_skills= ("conduite",),
        optional_skills=("Beginner", "Intermediate", "Expert"),
        days_in_schedule=28,
        employee_count=47,
        optional_skill_distribution=(
            CountDistribution(count=1, weight=3),
            CountDistribution(count=2, weight=1)
        ),
        shift_count_distribution=(
            CountDistribution(count=1, weight=0.5),
            CountDistribution(count=2, weight=0.3),
            CountDistribution(count=3, weight=0.2)
        ),
        availability_count_distribution=(
            CountDistribution(count=5, weight=4),
            CountDistribution(count=10, weight=3),
            CountDistribution(count=15, weight=2),
            CountDistribution(count=20, weight=1)
        ),
        random_seed=37
    )
}


FIRST_NAMES = (
    "Guindo", "Amy", "Beth", "Carl", "Dan", "Elsa", "Flo", "Gus", "Hugo",
    "Ivy", "Jay", "Kelly", "Laura", "Mona", "Nina43", "Oscar", "Paul", "Quinn",
    "Rita", "Sam", "Tina", "Uma", "Vince", "Will", "Xena", "Yara", "Zack",
    "Alice", "Brian", "Cleo", "Dylan", "Evan", "Fiona", "George", "Hanna",
    "Ian", "Jill", "Kevin", "Liam", "Megan", "Nancy", "Owen", "Peter", "Quincy",
    "yoan", "Mos", "kadja", "kaba", "mamdou", "bineta", "Adam", "Ben", "Charlie",
    "David", "Eva", "Frank", "Grace", "Helen", "Isla", "Jack", "Kara", "Leo",
    "Max", "Nina11", "Olivia", "Pauline", "Quincypo", "Rob", "Steve", "Toby", "Ursula",
    "Victor", "Walter", "Xander", "Yasmine", "Zoe", "Aaron", "Beatrice", "Catherine",
    "Danielle", "Elliot", "Felicity", "Gabriel", "Hannah", "Ianoi", "Jasper", "Kim",
    "Lily", "Matthew", "Natalie", "Oscarpo", "Peterpo", "Quinton", "Rory", "Sophie",
    "Tess", "Uma", "Vera", "Willow", "Ximena", "Yvette", "Zachary", "Alison", "Blake",
    "Cory", "Dexter", "Eleanor", "Florence", "Greg", "Helena", "Indigo", "Jasmine",
    "Kenneth", "Luca", "Mandy", "Nolan", "Oliver", "Quinnui", "Rachel", "Seth",
    "Tanya", "Ulrich", "Vivian", "Wendy", "Xandertr", "Yaraoi", "Zane", "Alex", "Brooke",
    "Clara", "Dylatyn", "Elliotr", "Faith", "Gina", "Hank", "Iris", "Jake", "Kurt",
    "Lori", "Megank", "Nina21", "Omar", "Penny", "Quinnr", "Rex", "Shelly", "Tracy", "Vance","Yasmin", "Zander"
)


LAST_NAMES = (
    "Hussen", "Cole", "Fox", "Green", "Jones", "King", "Li", "Poe", "Rye",
    "Smith", "Watt", "Black", "Brown", "Clark", "Davis", "Evans", "Garcia",
    "Hill", "Johnson", "Lee", "Martin", "Nelson", "Parker", "Roberts",
    "Taylor", "Walker", "White", "Young", "Adams", "Baker", "Carter", "Dixon",
    "Edwards", "Foster", "Griffin", "Harris", "Jackson", "Khan", "Lewis",
    "Mitchell", "Murphy", "Patel", "Scott", "Turner", "Wilson", "Wright",
    "hugues", "junior", "lat", "kkb", "Allen", "Bennett", "Chapman", "Dawson",
    "Ellis", "Ford", "Gibson", "Harrison", "Ishmael", "Jenkins", "Kelley", "Lawson",
    "Morris", "Nash", "ONeil", "Patterson", "Quinn", "Robinson", "Simmons", "Taylor",
    "Upton", "Vaughn", "Wells", "Xander", "Yates", "Zane", "Abrams", "Brooks", "Chavez",
    "Douglas", "PoEvans", "Flynn", "Greene", "Hayes", "Irwin", "LeJackson", "Kane", "Lloyd",
    "Marshall", "PoNelson", "Owen", "Perry", "Riley", "Shaw", "PoTaylor", "Underwood",
    "Vince", "West", "Xanderer", "Yale", "Zimmerman", "Alvarez", "PoBaker", "Collins",
    "Decker", "Fisher", "Graham", "Howard", "Ingram", "PoJones", "Knox", "Lambert",
    "Mack", "Norris", "Oliver", "poParker", "poQuinn", "Reed", "Shawqw", "Thomas", "Usher",
    "Vogel", "Wagner", "Xenakis", "Youngpo", "Ziegler", "Anderson", "Benson", "Curtis",
    "Donovan", "Elliott", "Fletcher", "pGraham", "Hawkins", "Irving", "James", "Kingpo",
    "Luna", "Miller", "Newton", "Olsen", "Peters", "Quincy", "Reedpo", "Summers", "Travis",
    "Urban", "Vera", "Whitaker", "Xanderpo"
)


USER_NAMES = [f"driver_{first} {last}" for first, last in zip(FIRST_NAMES, LAST_NAMES)]
SHIFT_LENGTH = timedelta(hours=8)
MORNING_SHIFT_START_TIME = time(hour=6, minute=0)
DAY_SHIFT_START_TIME = time(hour=9, minute=0)
AFTERNOON_SHIFT_START_TIME = time(hour=14, minute=0)
NIGHT_SHIFT_START_TIME = time(hour=22, minute=0)

SHIFT_START_TIMES_COMBOS = (
    (time(hour=6), time(hour=14), time(hour=23)), 
)


location_to_shift_start_time_list_map = dict()


def earliest_monday_on_or_after(target_date: date) -> date:
    """
    Retourne la date du prochain lundi à partir d'une date donnée.

    :param target_date: La date de départ.
    :return: La date du prochain lundi.
    """
    days = (7 - target_date.weekday()) % 7
    return target_date + timedelta(days=days)


def generate_demo_data(demo_data_or_parameters: DemoData | DemoDataParameters) -> EmployeeSchedule:
    """
    Génère des données démo en assignant des compétences, localisations
    et horaires à un ensemble d'employés.

    :param demo_data_or_parameters: Soit un type `DemoData`, soit un objet `DemoDataParameters`.
    :return: Objet contenant les données d'employés générées.
    """
    global location_to_shift_start_time_list_map, demo_data_to_parameters

    if isinstance(demo_data_or_parameters, DemoData):
        parameters = demo_data_to_parameters[demo_data_or_parameters]
    else:
        parameters = demo_data_or_parameters

    start_date = earliest_monday_on_or_after(date.today())  
    shift_template_index = 0

    for location in parameters.locations:
        location_to_shift_start_time_list_map[location] = SHIFT_START_TIMES_COMBOS[shift_template_index]
        shift_template_index = (shift_template_index + 1) % len(SHIFT_START_TIMES_COMBOS)

    employees = []
    random = Random(parameters.random_seed)
    for i in range(parameters.employee_count):
        j = random.randint(0, len(parameters.optional_skills) - 1)
        optional_skill = parameters.optional_skills[j]
        skills = [optional_skill]

        employees.append(
            Employee(name=USER_NAMES[i], skills=set(skills))
        )

    shifts = []
    ids = id_generator()
    
    for i in range(parameters.days_in_schedule):
        count, = random.choices(population=counts(parameters.availability_count_distribution),
                                weights=weights(parameters.availability_count_distribution))
        employees_with_availabilities_on_day = random.sample(employees, count)
        current_date = start_date + timedelta(days=i)
        for employee in employees_with_availabilities_on_day:
            rand_num = random.randint(0, 2)
            if rand_num == 0:
                employee.unavailable_dates.add(current_date)
            elif rand_num == 1:
                employee.undesired_dates.add(current_date)
            elif rand_num == 2:
                employee.desired_dates.add(current_date)
        shifts += generate_shifts_for_day(parameters, current_date, ids, all_predictions, start_date)

    for shift in shifts:
        if shift.location in ("première_classe", "affaire"):
            shift.required_skill = "Expert"
        elif shift.location == "mono_space":
            shift.required_skill = "Beginner"
        elif shift.location == "confort":
            shift.required_skill = "Intermediate"
    
    shift_count = 0
    for shift in shifts:
        shift.id = str(shift_count)
        shift_count += 1

    return EmployeeSchedule(employees=employees, shifts=shifts)


def generate_shifts_for_day(parameters: DemoDataParameters, current_date: date, ids: Generator[str, any, any],
                            all_predictions: dict, start_date: date) -> List[Shift]:
    """
    Génère les shifts pour une journée donnée.

    Args:
        parameters (DemoDataParameters): Les paramètres de configuration des données démo, 
                                         incluant les locations et les compétences requises.
        current_date (date): La date actuelle pour laquelle les shifts sont générés.
        ids (Generator[str, any, any]): Un générateur pour produire des identifiants uniques pour les shifts.
        all_predictions (dict): Les prédictions contenant le nombre attendu de tâches par plage horaire.
        start_date (date): La date de début des données de prédictions.

    Returns:
        List[Shift]: Une liste de shifts générés pour la journée.
    """
    global location_to_shift_start_time_list_map
    shifts = []

    for location in parameters.locations:
        shift_start_times = location_to_shift_start_time_list_map[location]

        for start_time in shift_start_times:
            shift_start_date_time = datetime.combine(current_date, start_time)
            shift_end_date_time = shift_start_date_time + SHIFT_LENGTH
            shifts += generate_shifts_for_timeslot(parameters, shift_start_date_time, shift_end_date_time, location, ids, current_date, all_predictions, start_date)

    return shifts


def generate_shifts_for_timeslot(parameters: DemoDataParameters, timeslot_start: datetime, timeslot_end: datetime,
                                 location: str, ids: Generator[str, any, any], current_date: date,
                                 all_predictions: dict, start_date: date) -> List[Shift]:
    
    """
    Génère les shifts pour une plage horaire spécifique.

    Args:
        parameters (DemoDataParameters): Les paramètres de configuration des données démo.
        timeslot_start (datetime): L'heure de début de la plage horaire.
        timeslot_end (datetime): L'heure de fin de la plage horaire.
        location (str): L'emplacement pour lequel les shifts sont générés.
        ids (Generator[str, any, any]): Un générateur pour produire des identifiants uniques pour les shifts.
        current_date (date): La date actuelle pour laquelle les shifts sont générés.
        all_predictions (dict): Les prédictions contenant le nombre attendu de tâches par plage horaire.
        start_date (date): La date de début des données de prédictions.

    Returns:
        List[Shift]: Une liste de shifts générés pour la plage horaire.
    """
    shifts = []
    random = Random(parameters.random_seed)
    time_range = determine_time_range(timeslot_start)

    # Obtenir les prédictions pour ce créneau et cette date
    predefined_shifts = get_predefined_shifts(all_predictions, time_range, current_date, start_date)

    # Répartition aléatoire des tâches sur les locations
    location_shift_counts = distribute_shifts_among_locations(predefined_shifts, parameters.locations, random)

    # Générer les shifts pour chaque location
    for _ in range(location_shift_counts[location]):
        required_skill = parameters.required_skills
        shifts.append(Shift(
            id=next(ids),
            start=timeslot_start,
            end=timeslot_end,
            location=location,
            required_skill='',
            optional_skill=required_skill
        ))

    return shifts


def distribute_shifts_among_locations(total_shifts: int, locations: List[str], random: Random) -> dict:
    """
    Répartit le nombre total de shifts entre plusieurs emplacements de manière aléatoire.

    Args:
        total_shifts (int): Le nombre total de shifts à répartir.
        locations (List[str]): La liste des emplacements disponibles.
        random (Random): Instance de générateur de nombres aléatoires.

    Returns:
        dict: Un dictionnaire avec les emplacements comme clés et le nombre de shifts comme valeurs.
    """
    location_shift_counts = {location: 0 for location in locations}

    # Distribuer les tâches aléatoirement entre les locations
    for _ in range(total_shifts):
        selected_location = random.choice(locations)
        location_shift_counts[selected_location] += 1

    return location_shift_counts


def determine_time_range(start_time: datetime) -> str:
    """
    Détermine la plage horaire correspondant à une heure de début donnée.

    Args:
        start_time (datetime): L'heure de début d'une plage horaire.

    Returns:
        str: La plage horaire sous forme de chaîne, par exemple "6h-14h".
    """
    if time(hour=6) <= start_time.time() < time(hour=14):
        return "6h-14h"
    elif time(hour=14) <= start_time.time() < time(hour=23):
        return "14h-23h"
    else:
        return "23h-5h"


def get_predefined_shifts(all_predictions: dict, time_range: str, current_date: date, start_date: date) -> int:
    """
    Obtient le nombre prédéfini de shifts pour une plage horaire et une date spécifique.

    Args:
        all_predictions (dict): Les prédictions contenant le nombre de shifts par plage horaire et par jour.
        time_range (str): La plage horaire cible (par exemple, "6h-14h").
        current_date (date): La date actuelle pour laquelle les prédictions sont utilisées.
        start_date (date): La date de début des prédictions.

    Returns:
        int: Le nombre de shifts prédéfini pour cette plage horaire et cette date.
    """
    # Calcul de l'index basé sur la différence en jours avec le lundi de départ
    days_since_start = (current_date - start_date).days

    # Vérifier si l'index est valide pour les données disponibles
    if days_since_start < 0 or days_since_start >= len(all_predictions[time_range]):
        return 0  # Retourner 0 si la date est en dehors de l'intervalle des prédictions

    return all_predictions[time_range][days_since_start]["value"]


def id_generator():
    """
    Génère un identifiant unique incrémental sous forme de chaîne.

    Yields:
        str: Un identifiant unique.
    """
    current_id = 0
    while True:
        yield str(current_id)
        current_id += 1