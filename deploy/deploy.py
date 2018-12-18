from pa.bin import deploy_sh


deploy_sh('LNetwork',
          ['../LNetwork/__manifest__.py'],
          'config.conf',
          ['../'],
          {
              'uwsgi_parasite.ini': '',
              'start.sh': ''
          })
