from __future__ import annotations
from typing import List, Dict, Optional, Set

from dataclasses import dataclass, field

# Sample use
# m = Meta()
# tbl = Table(name="student")
# tbl.columns = [Column(name="id", table = tbl, data_type = "varchar", is_pk = true),
#                Column(name="name",...)
#               ]
# m.tables[tbl.name] = tbl

# tbl = Table(name="department")
# tbl.columns = [Column(name="department_name", table = tbl, data_type = "varchar", is_pk = true),
# m.tables[tbl.name] = tbl
# 
# m.tables["student"].refersTo.append(m.tables["department"])


@dataclass
class Meta:
    tables: Dict[str, Table] =  field(default_factory=dict)

@dataclass
class Table:
    name: str
    schema: str = ''
    columns: List[Column] = field(default_factory=list)
    refersTo: List[Table] = field(default_factory=list) # foreign key relationships

    def primaryKey(self):
        return [col for col in self.columns.values() if col.is_pk]
    
@dataclass
class Column:
    "An instance of Column represents a column of a given table"
    name: str
    table: Table
    data_type: str
    is_pk : bool   # true if this col is part of a pk (or singly so)


