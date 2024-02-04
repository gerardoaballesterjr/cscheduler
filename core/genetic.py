import random, datetime, dataclasses, random, typing, itertools
from core import data, models

@dataclasses.dataclass
class Gene:
    section: models.Section
    assign: models.Assign = None
    days: typing.List[models.Day] = dataclasses.field(default_factory=list)
    stime: str = None
    etime: str = None
    room: models.Room = None

    def create_days(self):
        if not self.assign.days.all():
            if self.assign.subject.type == 'Minor':
                self.days = random.choice(data.days0)
            elif self.assign.subject.hours < 3:
                self.days = random.choice(data.days1)
            else:
                if self.assign.subject.hours > 5:
                    self.days = random.choice(data.days2[:3])
                else:
                    self.days = random.choice(data.days2)

    def create_time(self):
        duration = self.assign.subject.hours if len(self.days) == 1 else self.assign.subject.hours / len(self.days)
        time = random.choice(data.hours[str(duration)])
        self.stime = time[0]
        self.etime = time[1]

    def get_room(self):
        try:
            self.room = models.Room.objects.filter(type=self.assign.subject.room_type).order_by('?').first()
        except models.Room.DoesNotExist:
            self.room = None

@dataclasses.dataclass
class Population:
    genes: typing.List[Gene] = dataclasses.field(default_factory=list)
    conflict: int = 0

    def overlap(self, gene0: Gene, gene1: Gene):
        def time_to_minutes(time: str):
            hours, minutes = map(int, time.split(':'))
            return hours * 60 + minutes
        gene0_stime = time_to_minutes(gene0.stime)
        gene0_etime = time_to_minutes(gene0.etime)
        gene1_stime = time_to_minutes(gene1.stime)
        gene1_etime = time_to_minutes(gene1.etime)

        time = bool((gene0_stime < gene1_etime and gene0_etime > gene1_stime) or (gene1_stime < gene0_etime and gene1_etime > gene0_stime))
        days = bool(set(gene0.days).intersection(set(gene1.days)))
        room = bool(gene0.room == gene1.room)
        professor = bool(gene0.assign.professor == gene1.assign.professor)
        section = bool(gene0.section == gene1.section)
        
        if gene0.room.type.name == gene1.room.type.name == 'Online':
            return bool(time and days and professor) or bool(time and days and section)
        else:
            return bool(time and days and professor and room) or bool(time and days and section and room) or bool(time and days and professor) or bool(time and days and section)

    
    def professor_room_section_conflict(self):
        for gene0, gene1 in itertools.combinations(self.genes, 2):
            if self.overlap(gene0, gene1):
                self.conflict += 1
        
        for gene0 in self.genes:
            for schedule in models.Schedule.objects.filter(section__semester=gene0.section.semester):
                gene1 = Gene(
                    section = schedule.section,
                    assign = schedule.assign,
                    days = list(schedule.days.all()),
                    stime = schedule.stime,
                    etime = schedule.etime,
                    room = schedule.room,
                )

                if self.overlap(gene0, gene1):
                    self.conflict += 1

    def time_conflict(self):
        for gene in self.genes:
            stime = datetime.datetime.strptime(gene.stime, '%H:%M')
            etime = datetime.datetime.strptime(gene.etime, '%H:%M')
            if float(float((etime-stime).total_seconds()/3600.0)*len(gene.days)) != gene.assign.subject.hours:
                self.conflict += 1

@dataclasses.dataclass
class Generation:
    populations: typing.List[Population] = dataclasses.field(default_factory=list)

    def sort(self):
        self.populations = sorted(self.populations, key=lambda x: x.conflict)

@dataclasses.dataclass
class Genetic:
    semester: models.Semester
    user: models.User = None
    max_population: int = 20
    max_generation: int = 1000
    mutation_rate: float = 0.5
    generations: typing.List[Generation] = dataclasses.field(default_factory=list)
    error: str = None

    def initialize(self):
        generation = Generation()
        for _ in range(self.max_population):
            population = Population()
            if self.error:
                break
            for section in models.Section.objects.filter(semester=self.semester, course__department=self.user.department):
                if self.error:
                    break
                for subject in section.subjects.all():
                    assign = models.Assign.objects.filter(semester=self.semester, subject=subject).order_by('?').first()
                    if assign is not None:
                        gene = Gene(assign=assign, section=section)
                        gene.create_days()
                        gene.create_time()
                        gene.get_room()
                        if gene.room is None:
                            self.error = f'Can\'t find a room for this subject \'{subject.name}\'.'
                            break
                        population.genes.append(gene)
                    else:
                        self.error = f'This subject \'{subject.name}\' has not been assigned yet.'
                        break
            generation.populations.append(population)
        self.generations.append(generation)

    def evaluate(self):
        for population in self.generations[-1].populations:
            population.conflict = 0
            population.professor_room_section_conflict()
            population.time_conflict()
        self.generations[-1].sort()

    def crossover(self):
        old_generation = self.generations[-1]
        new_generation = Generation()
        [new_generation.populations.append(old_generation.populations.pop(0)) for _ in range(2)]
        while len(old_generation.populations) != 0:
            old_population0 = old_generation.populations.pop(0)
            old_population1 = old_generation.populations.pop(-1)
            split_point = int(len(old_population0.genes) // 2)
            new_population0 = Population()
            new_population0.genes = old_population0.genes[:split_point] + old_population1.genes[split_point:]
            new_generation.populations.append(new_population0)
            new_population1 = Population()
            new_population1.genes = old_population1.genes[:split_point] + old_population0.genes[split_point:]
            new_generation.populations.append(new_population1)
        self.generations.append(new_generation)

    def mutate(self):
        for population in self.generations[-1].populations[2:]:
            if random.random() < self.mutation_rate:
                gene = population.genes[population.genes.index(random.choice(population.genes))]
                gene.assign = models.Assign.objects.filter(semester=self.semester, subject=gene.assign.subject).order_by('?').first()
                gene.create_days()
                gene.create_time()
                gene.get_room()
        self.generations.pop(0)

    def solution(self):
        return [population.conflict for population in self.generations[-1].populations if population.conflict == 0]
    
    def save(self):
        for gene in self.generations[-1].populations[0].genes:
            schedule = models.Schedule(
                stime = gene.stime,
                etime = gene.etime,
                room = gene.room,
                assign = gene.assign,
                section = gene.section,
            )
            schedule.save()
            [schedule.days.add(day) for day in gene.days]    