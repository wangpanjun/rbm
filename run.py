#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from rbm import main

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    main.app.debug = True
    main.app.run(port=port, host='0.0.0.0')
