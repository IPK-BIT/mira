import json
import polars as pl
from sqlalchemy.orm import Session

from db.models.models import ObservationVariable
from db.schemas import phenotyping

def load_variables(db: Session, filename: str):
    traits = pl.read_csv(filename, separator='\t')
    for t in traits.iter_rows(named=True):
        trait = phenotyping.Trait(
            traitDbId=t['Trait'],
            traitPUI=t['Trait Accession Number'],
            traitClass=t['Trait Class'] if t['Trait Class'] else None,
        )
        method = phenotyping.Method(
            methodDbId=t['Method'],
            methodPUI=t['Method Accession Number'],
            description=t['Method Description'],
        )

        categories = []
        if not t['Scale Values'] == None:
            for value in t['Scale Values'].split(';'):
                categories.append(phenotyping.ScaleValue(
                    value=value.split(':')[0],
                    label=value.split(':')[1]
                ))

        scaleValues = phenotyping.ScaleValues(
            categories=categories,
        )
        scale = phenotyping.Scale(
            scaleDbId=t['Scale'],
            scalePUI=t['Scale Accession Number'],
            dataType=t['Scale Type'],
            validValues=scaleValues
        )
        variable = ObservationVariable(
            observationVariableDbId=t['Variable ID'],
            observationVariableName=t['Variable Name'],
            observationVariablePUI=t['Variable Accession Number'],
            trait=json.dumps(trait.model_dump()),
            method=json.dumps(method.model_dump()),
            scale=scale.model_dump(),
        )
        db.add(variable)
    db.commit()