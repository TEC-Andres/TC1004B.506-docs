FROM texlive/texlive:latest-medium

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 inkscape \
    && rm -rf /var/lib/apt/lists/*

# scheme-medium ships only the small scheme; the TDP document needs the LaTeX
# extra/bibliography/language collections on top of it.
RUN tlmgr install \
      collection-latexextra \
      collection-latexrecommended \
      collection-bibtexextra \
      collection-langspanish \
      collection-pictures \
      collection-fontsrecommended \
      biber

WORKDIR /workspace

COPY .latex-compiler/src ./src
COPY .github/docker/patch_texmake_case.py /tmp/patch_texmake_case.py
RUN python3 /tmp/patch_texmake_case.py /workspace/src/texmake.py \
    && rm /tmp/patch_texmake_case.py

CMD ["bash"]
