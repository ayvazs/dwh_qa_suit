from django.db import models
from django.urls import reverse
from django.utils import timezone
import pyodbc
# Create your models here.


class Connection(models.Model):
    connection_name = models.CharField(max_length = 100, null = False, default = 'Name your data source!')
    connection_string = models.CharField(max_length = 1000, null = False, default = 'Put connection string here!')

    def __str__(self):
        return self.connection_name

    def get_absolute_url(self):
        return reverse('dwh_qa_core:connection_detail', kwargs = {'pk': self.pk})


class TestSet(models.Model):
    set_name = models.CharField(max_length = 100, null = False, default = 'Name your set!')

    def __str__(self):
        return self.set_name

    def get_absolute_url(self):
        return reverse('dwh_qa_core:set_detail', kwargs = {'pk': self.pk})

    def get_tests_quantity(self):
        return self.tests.all().count()

    def get_tests_succeeded_quantity(self):
        quantity = 0
        for test in self.tests.all():
            if test.is_succeeded():
                quantity += 1
        return quantity

    def get_tests_failed_quantity(self):
        quantity = 0
        for test in self.tests.all():
            if not test.is_succeeded():
                quantity += 1
        return quantity

    def get_status(self):
        tests_qty = self.get_tests_quantity()
        status = 0.0
        if tests_qty > 0 :
            status = self.get_tests_succeeded_quantity() / tests_qty
        return status * 100


class Test(models.Model):
    test_set = models.ForeignKey(TestSet, related_name = 'tests')
    check_cnx = models.ForeignKey(Connection, related_name = 'check_connection')
    right_cnx = models.ForeignKey(Connection, related_name = 'right_connection')
    test_name = models.CharField(max_length = 200, null = False, default = 'Name your test!')
    test_ts_start = models.DateTimeField(null = True)
    test_ts_finish = models.DateTimeField(null = True)
    check_query = models.CharField(max_length = 4000)
    check_query_result = models.BigIntegerField(null = True)
    check_query_error_msg = models.CharField(max_length = 4000)
    right_query = models.CharField(max_length = 4000)
    right_query_result = models.BigIntegerField(null = True)
    right_query_error_msg = models.CharField(max_length = 4000)

    def __str__(self):
        return self.test_name

    def get_absolute_url(self):
        return reverse('dwh_qa_core:test_detail', kwargs = {'testset_id':self.test_set.id, 'pk': self.pk})

    def execute(self):
        self.test_ts_start = timezone.now()
        # Right part #
        try:
            connection = pyodbc.connect(self.right_cnx.connection_string)
        except Exception as exc:
            self.right_query_error_msg = exc.args[1]
        else:
            self.right_query_error_msg = 'OK'
            cursor = connection.cursor()
            try:
                self.right_query_result = cursor.execute(self.right_query).fetchval()
            except Exception as exc:
                self.right_query_result = None
                self.right_query_error_msg = exc.args[1]


        # Check part #
        try:
            connection = pyodbc.connect(self.check_cnx.connection_string)
        except Exception as exc:
            self.check_query_error_msg = exc.args[1]
        else:
            self.check_query_error_msg = 'OK'
            cursor = connection.cursor()
            try:
                self.check_query_result = cursor.execute(self.check_query).fetchval()
            except Exception as exc:
                self.check_query_result = None
                self.check_query_error_msg = exc.args[1]

        self.test_ts_finish = timezone.now()

    def is_succeeded(self):
        result = False
        if self.right_query_result == self.check_query_result and self.right_query_result is not None:
            result = True
        return result
