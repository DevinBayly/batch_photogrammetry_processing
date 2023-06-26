from pathlib import Path

import tarfile

ar = tarfile.open("ortho_out.tar.gz","w:gz")
orthos = sorted(Path("../tmp").glob("*/odm_orthophoto/odm_orthophoto.tif"))
print(orthos,len(orthos))
for o in orthos:
  ar.add(str(o))


ar.close()

