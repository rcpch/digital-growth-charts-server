import rcpchgrowth.rcpchgrowth as rcpchgrowth
# from .calculations import create_measurement_object
import numpy as np
import os
from datetime import datetime
from flask import jsonify



    """
    Return object structure

    [
        "height": [
            {
                sds: -2.666666,
                uk90_child_data:[.....],
                uk90_preterm_data: [...],
                who_child_data: [...],
                who_infant_data: [
                    {
                        label: 0.4, `this is the centile
                        x: 4, `this is the decimal age
                        y: 91.535  `this is the measurement
                    }
                ]
            }
        ],
        ... repeat for weight, bmi, ofc, based on which measurements supplied. If only height data supplied, only height centile data returned
    ]

    """
