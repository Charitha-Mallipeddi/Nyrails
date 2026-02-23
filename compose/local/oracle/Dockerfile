FROM gvenzl/oracle-free:23-slim
COPY --chown=oracle:oinstall --chmod=0755 compose/local/oracle/container-entrypoint.sh /opt/oracle/container-entrypoint-new.sh
USER oracle
# WORKDIR ${ORACLE_BASE}
ENTRYPOINT ["container-entrypoint-new.sh"]
