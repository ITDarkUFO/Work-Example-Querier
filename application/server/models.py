from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Person(models.Model):
    '''Список сотрудников, которые участвуют в остальных моделях.'''
    uuid = models.UUIDField(verbose_name='UUID сотрудника', max_length=50, unique=True, default=None,
                            help_text="Можно узнать в системе ТЕЗИС, либо в отладке отчетов приложения.")
    name = models.CharField(verbose_name='Имя сотрудника', max_length=100,
                            help_text="Имя сотрудника, как оно записано в системе ТЕЗИС.")

    class Meta:
        verbose_name = 'сотрудник'
        verbose_name_plural = 'сотрудники'
        ordering = ['name']

    def __str__(self):
        return self.name


class ReportKid(models.Model):
    person = models.OneToOneField(to=Person, on_delete=models.CASCADE, default=None,
                                  verbose_name='Сотрудник', help_text="Сотрудник, который будет будет отображаться в отчете КИД.",
                                  error_messages={'unique': 'Этот сотрудник уже есть в таблице исполнителей КИД.'})

    class Meta:
        verbose_name = 'исполнитель КИД'
        verbose_name_plural = 'исполнители КИД'
        ordering = ['person']

    def __str__(self):
        return self.person.name


class AssignmentsSources(models.Model):
    '''Источники поручений и важность их поручений.'''
    assignment_source = models.CharField(verbose_name='Источник поручения', max_length=500,
                                         unique=True, help_text='Источник поручения, учитываемый в расчете КИД.')
    coefficient = models.PositiveIntegerField(verbose_name='Важность поручения', validators=[
                                              MinValueValidator(1), MaxValueValidator(3)], default=1, help_text='Важность поручения от 1 до 3.')

    class Meta:
        verbose_name = 'источник поручений'
        verbose_name_plural = 'источники поручений'
        ordering = ['-coefficient', 'assignment_source']

    def __str__(self):
        return self.assignment_source


class ExcludedOrganizations(models.Model):
    '''Список организаций, которые не должны присутствовать в отчетах.'''
    name = models.CharField(verbose_name='Название организации', max_length=500, unique=True,
                            help_text="Название организации, которая будет исключена из отчетов.")

    class Meta:
        verbose_name = 'исключенная организация'
        verbose_name_plural = 'исключенные организации'
        ordering = ['name']

    def __str__(self):
        return self.name


class AssignmentsInitiators(models.Model):
    '''Список инициаторов поручений.'''
    person = models.OneToOneField(to=Person, on_delete=models.CASCADE, default=None,
                                  verbose_name='Сотрудник', help_text="Сотрудник, поручения которого будут учитываться в КИД.",
                                  error_messages={'unique': 'Этот сотрудник уже есть в таблице инициаторов КИД.'})

    class Meta:
        verbose_name = 'инициатор КИД'
        verbose_name_plural = 'инициаторы КИД'
        ordering = ['person']

    def __str__(self):
        return self.person.name


class CuratorsKid(models.Model):
    '''Список кураторов поручений.'''
    curator = models.OneToOneField(
        to=Person, related_name='curator', on_delete=models.CASCADE, verbose_name='Куратор', help_text='Сотрудник, которому будут прибавляться поручения его подчиненных.', error_messages={'unique': 'Этот сотрудник уже есть в таблице кураторов КИД.'})
    dependants = models.ManyToManyField(
        to=Person, related_name='dependants', verbose_name='Подчиненные')

    def get_dependants(self):
        return f'{len(self.dependants.all())}: ' + ', '.join(d.name for d in self.dependants.all())

    class Meta:
        verbose_name = 'куратор КИД'
        verbose_name_plural = 'кураторы КИД'
        ordering = ['curator']

    def __str__(self):
        return self.curator.name


class DeputyGovernor(models.Model):
    '''Список заместителей губернатора'''
    person = models.OneToOneField(to=Person, on_delete=models.CASCADE, default=None,
                                  verbose_name='Заместитель губернатора', help_text="Заместитель губернатора, который будет отображаться в отчете КИД.",
                                  error_messages={'unique': 'Этот сотрудник уже есть в таблице исполнителей КИД.'})

    class Meta:
        verbose_name = 'заместитель губернатора'
        verbose_name_plural = 'заместители губернатора'
        ordering = ['person']

    def __str__(self):
        return self.person.name


class Minister(models.Model):
    '''Список министров'''
    person = models.OneToOneField(to=Person, on_delete=models.CASCADE, default=None,
                                  verbose_name='Министр', help_text="Министр, который будет отображаться в отчете КИД.",
                                  error_messages={'unique': 'Этот сотрудник уже есть в таблице исполнителей КИД.'})

    class Meta:
        verbose_name = 'министр'
        verbose_name_plural = 'министры'
        ordering = ['person']

    def __str__(self):
        return self.person.name
