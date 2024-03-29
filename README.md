# ReuniceWP3

Development about a portail that help to interrogates the different open science repository of the REUNICE project partners.

Here are the open science portals to access to the articles of the partners :

Partner | City/Country | Open Digital Repository | Tool | Extraction of data | Accessible via API | Query customizable via API
------- | ------------ | ----------------------- | ---- | ------------------ | ------------------ | -------------------------
UPHF | Valenciennes/France | [uphf.hal.science](https://uphf.hal.science/) | HAL | Yes | Yes | Yes
UC | Cantabria/Spain | [repositorio.unican.es](https://repositorio.unican.es/xmlui/) | DSpace | Yes | Yes | No
BUT | Brandenburg/Germany | [opus4.kobv.de/opus4-btu](https://opus4.kobv.de/opus4-btu/home) | OPUS-4 | Yes | No | No
UNICT | Catania/Italy | [iris.unict.it](https://www.iris.unict.it/) | IRIS | Yes | No | No
PUT | Poznan/Poland | [sin.put.poznan.pl](https://sin.put.poznan.pl/) | SINUS | Yes | No | No
UVA | Vaasa/Finland | [osuva.uwasa.fi](https://osuva.uwasa.fi/) | DSpace | No | **No?** | No
UMons | Mons/Belgium | [orbi.umons.ac.be](https://orbi.umons.ac.be/) | Orbi | No | No | No


---

Regarding the WP3 package,the objective is to interrogate the REUNICE Open Science portals to find similar articles as ours.
- The idea was to interrogate directly through a program the different portals.. But it is only possible (from the information we get from the OS portals) with UC (Repositorio/Dspace) and UPHF (Hal).
- Another solution is to periodically (1/month) build a database manually with the articles created by each partner  and to interrogate it… Its is a long and repetitive task..


For the moment, only 2 portals can be interrogated via a software :
- In [requetesUVHC_HAL](./requetesUVHC_HAL.ipynb) you can find how to interrogate HAL(UPHF) portal via python.
- In [requetesUC_DSPACE](./requetesUC_DSPACE.ipynb) you can find how to interrogate DSpace(UC) portal via python.
  - N.B. BUT uses also DSpace, but this version cannot be interrogated via an API (for the moment)

do not hesitate to contact emmanuel.adam-at-uphf.fr if you have any advice...

Best regards..



----