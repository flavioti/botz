import logging

from dynaconf import Dynaconf

logger = logging.getLogger(__name__)

settings = Dynaconf(
    environments=True,
    env_switcher="ENV_MODE",
    settings_files=[
        "settings.yaml",
        ".secrets.yaml",
    ],
    core_loaders=["YAML"],
    includes=[],
)

logger.info(settings)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
