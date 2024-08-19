"""

:module:    test_data_model.py
:author:    GM (genuinemerit @ pm.me)

Saskan Data Management middleware.
"""

import json
import random
import string
from pprint import pformat as pf  # noqa: F401
from pprint import pprint as pp  # noqa: F401

from data_structs import EntityType
from method_files import FileMethods
from method_shell import ShellMethods

FM = FileMethods()
SM = ShellMethods()


class TestDataModel(object):
    """
    Managem test data rows on database
    """

    def __init__(self):
        """Initialize TestData object."""
        self.test_data_rows = 1
        self.table_name: str = ''
        self.sql_cols: list = []
        self.num_cols: int = 0
        self.ck_constraints: dict = {}
        self.fk_constraints: dict = {}

# =============================================================
# Algorithm-based TestData objects
# =============================================================
# =============================================================
# Abstracted 'private' methods
# =============================================================
    def _get_data_model(self,
                        DB: object,
                        p_data_model: object) -> bool:
        """Get data model info from object and CREATE SQL file.
        :args:
        - DB - current instance of the DB object.
        - p_data_model: object.
        :sets:
        - class level attributes
        """
        self.table_name = p_data_model._tablename.upper()
        sql_create = DB.get_sql_file(f"CREATE_{self.table_name}")
        sql_line = sql_create.split('\n')
        self.sql_cols = [line.strip()[:-1] for line in sql_line
                         if not line.startswith(
                            ('--', 'CREATE', 'CHECK',
                             'FOREIGN', 'PRIMARY'))]
        self.num_cols = len(self.sql_cols)
        constraints = {k: v for k, v
                       in p_data_model.Constraints.__dict__.items()
                       if not k.startswith('_')}
        self.ck_constraints = constraints.get('CK', {})
        self.fk_constraints = constraints.get('FK', {})
        return True

    def _get_name_value(self,
                        p_row_num: int) -> str:
        """Return test data value for a name field
        :args:
        - p_row_num: int. Row number.
        :returns: str
        """
        v = f"test_{self.table_name.lower()}_{p_row_num:04d}"
        return v

    def _get_file_value(self) -> str:
        """Return test data value for a file field
        :returns: str
        """
        v = SM.get_cwd_home() + '/' + SM.get_uid()[10:17] + '/' +\
            random.choice(['test_data', 'other', 'config', 'backup']) +\
            random.choice(['.txt', '.jpg', '.png', '.pdf', '.dat', '.xls'])
        return v

    def _get_astro_value(self) -> float:
        """Return test data value for a kg, gly, gly3, pc3 field
        :returns: float
        """
        v = random.randint(1, 100000000000) / 1000
        return v

    def _get_rate_value(self) -> float:
        """Return test data value for a rate
        :returns: float
        """
        v = random.randint(1, 10000) / 10
        return v

    def _get_degree_value(self) -> float:
        """Return test data value for a degree
        :returns: float
        """
        v = random.randint(1, 1801) / 10
        if (random.randint(0, 1) == 0):
            v = -v
        return v

    def _get_xyz_value(self) -> float:
        """Return test data value for meters or x, y, z dimensions
        :returns: float
        """
        v = random.randint(1, 300) / 10
        return v

    def _get_fk_value(self,
                      DB: object,
                      p_col_nm: str) -> list:
        """Return test data value for a foreign key field
        :args:
        - DB - current instance of the DB object.
        - p_col_nm: str. Column name.
        :returns:
        - value from another table
        """
        v = None
        for fk_col, (rel_table, pk_col) in self.fk_constraints.items():
            if fk_col == p_col_nm:
                rel_data = DB.execute_select_all(rel_table)
                v = rel_data[pk_col]
                break
        return v

    def _get_uri_value(self) -> str:
        """Return test data value for a uri field
        :returns: str
        """
        v = 'https://' + SM.get_host() + '/' + SM.get_uid()[10:17] + '/' +\
            random.choice(['map', 'ideogram', 'sound', 'webby', 'picture']) +\
            random.choice(['.html', '.jpg', '.wav', '.pdf', '.dat', '.csv'])
        return v

    def _get_points_value(self) -> str:
        """Return test data value for a points field
        :returns: json-formatted str
        """
        points = []
        num_points = random.randint(3, 20)
        for _ in range(num_points):
            latitude = random.uniform(-90, 90)
            longitude = random.uniform(-180, 180)
            points.append((latitude, longitude))
        return json.dumps(points)

    def _get_text_value(self) -> str:
        """Return generic text value
        :returns: str
        """
        v = ''.join(random.choices(string.ascii_letters +
                                   string.digits,
                                   k=random.randint(10, 30)))
        return v

    def _get_hazards_or_features(self,
                                 p_entity: EntityType) -> str:
        """Return made-up data using a *_hazards or
            *_features EntityType and the following
        JSON format:
        [{"uid": int,
          "type": EntityType.RIVER_HAZARD,
          "loc": lat-long},
          ...]
        """
        hazfeats = []
        num_hazfeats = random.randint(1, 10)
        for _ in range(num_hazfeats):
            hazfeat = {}
            hazfeat["uid"] = random.randint(1000, 9999)
            hazfeat["type"] = random.choice(p_entity)
            hazfeat["loc"] = (random.uniform(-90, 90),
                              random.uniform(-180, 180))
            hazfeats.append(hazfeat)
        return json.dumps(hazfeats)

# =============================================================
# 'Public' methods
# =============================================================
    def make_algo_test_data(self,
                            DB: object,
                            p_data_model: object) -> tuple:
        """
        Create test data row(s) for specified table.
        :args:
        - DB: object. Current instance of the DB object.
        - p_data_model: object. Data model object
        :returns: tuple
        - Name of SQL script to insert test data.
        - List of tuple of values to be inserted.
        """
        full_list: list = []
        self._get_data_model(DB, p_data_model)

        print(f"\nGenerating test data for:  {self.table_name}...")

        for rx in range(self.test_data_rows):
            row_list: list = []
            for cx, col in enumerate(self.sql_cols):

                col_nm, col_type, _, col_default = col.split()
                row_list.append(col_default.replace("'", ""))

                if col_nm.endswith('_pk'):
                    row_list[cx] = SM.get_key()
                elif col_nm.endswith('_dttm'):
                    row_list[cx] = SM.get_iso_time_stamp()

                elif col_nm in self.ck_constraints.keys():
                    row_list[cx] = random.choice(self.ck_constraints[col_nm])
                elif col_nm in self.fk_constraints.keys():
                    row_list[cx] =\
                        random.choice(self._get_fk_value(DB, col_nm))

                elif col_nm.startswith('file_'):
                    row_list[cx] = self._get_file_value()
                elif col_nm.startswith('is_'):
                    row_list[cx] = random.choice([0, 1])
                elif col_nm.startswith('river_features_'):
                    row_list[cx] =\
                        self._get_hazards_or_features(
                            EntityType.RIVER_FEATURE)
                elif col_nm.startswith('river_hazards_'):
                    row_list[cx] =\
                        self._get_hazards_or_features(
                            EntityType.RIVER_HAZARD)
                elif col_nm.startswith('ocean_features_'):
                    row_list[cx] =\
                        self._get_hazards_or_features(
                            EntityType.OCEAN_FEATURE)
                elif col_nm.startswith('ocean_hazards_'):
                    row_list[cx] =\
                        self._get_hazards_or_features(
                            EntityType.OCEAN_HAZARD)

                elif col_nm.endswith('_name'):
                    row_list[cx] = self._get_name_value(rx)
                elif col_nm.endswith('_uri'):
                    row_list[cx] = self._get_uri_value()
                elif col_nm.endswith('_dg'):
                    row_list[cx] = self._get_degree_value()
                elif col_nm.endswith('_cnt'):
                    row_list[cx] = random.randint(10, 100)
                elif col_nm.endswith('_au'):
                    row_list[cx] = random.randint(9, 50) / 10

                elif '_points_' in col_nm:
                    row_list[cx] = self._get_points_value()

                elif any(col_nm.endswith(suffix)
                         for suffix in ('_px', '_pulse_per_ms',
                                        '_days')):
                    row_list[cx] = random.randint(30, 10000)
                elif any(col_nm.endswith(suffix)
                         for suffix in ('_rate', '_per_mpc',
                                        '_per_s', '_velocity')):
                    row_list[cx] = self._get_rate_value()
                elif any(col_nm.endswith(suffix)
                         for suffix in ('_kg', '_gly', '_gpc', '_pc',
                                        '_ly3', '_gyr', '_pc3', '_gpc3',
                                        '_gly3')):
                    row_list[cx] = self._get_astro_value()
                elif any(col_nm.endswith(suffix)
                         for suffix in ('_km', '_m', '_x', '_cnt', '_y',
                                        '_z', '_a', '_b', '_c', '_pitch',
                                        '_yaw', '_roll', '_gdy')):
                    row_list[cx] = self._get_xyz_value()

                elif col_type == 'BOOLEAN':
                    row_list[cx] = random.choice([0, 1])
                elif col_type == 'TEXT':
                    row_list[cx] = self._get_text_value()
                elif col_type == 'NUMERIC':
                    row_list[cx] = random.randint(20, 1000) / 10

            full_list.append(tuple(row_list))
        return (f'INSERT_{self.table_name}', full_list)
