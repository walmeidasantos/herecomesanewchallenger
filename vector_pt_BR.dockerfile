mkdir mypostgresql;
echo 'pgvector/pgvector:pg16
LABEL version="0.0.1"
LABEL name="vector_pr_BR"
LABEL description="PostgreSQL Vector pt_BR.UTF8"
RUN localedef -i pt_BR -c -f UTF-8 -A /usr/share/locale/locale.alias pt_BR.utf-8
ENV LANG pt_BR.utf8' > Dockerfile