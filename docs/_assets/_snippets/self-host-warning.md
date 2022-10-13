!!! danger "Self Hosting - Clinical Safety Risk"
    **TL;DR: Don't self-host in production. Use our warranted API**.

    The only version of the Digital Growth Charts API which is warranted to be correct for clinical use is that which is served by the RCPCH itself from our API endpoint at <https://api.rcpch.ac.uk>. While we have, for reasons of transparency, equity-of-access and safety, made it _possible_ to use our open source code to set up a server providing Digital Growth Charts API calculations, we specifically and strongly advise _against_ doing this, except for testing, verification, research (which is not for academic publication) or development purposes.
    
    **WE STRONGLY RECOMMEND NOT TO SELF-HOST THE SERVER FOR PRODUCTION, CLINICAL or other 'LIVE' USE.**  
    If self-hosting you would not have a warranty from RCPCH and your organisation would therefore be liable for misconfigurations in the server leading to clinical mishap. Growth Charts are complex, and in order to assure your service is safe, you are likely going to need a large amount of statistical, clinical and technical consultancy. You must understand and accept that any version of this API running **outside** our controlled environment must have been:
    
    1. Independently **technically** assured such that the platform, deployment, and modifications are secure, safe, and reliable.
    
    1. Independently **clinically** assured, such that the application is safe and has a qualified Clinical Safety Officer, a Clinical Safety Management File, and is fully compliant with DCB0129 and DCB0160.
   
    1. Registered with the MHRA as a Medical Device (for UK deployment) and EU MDR, with Declaration of Conformity (for EU deployment).
   
    **For this reason, we STRONGLY recommend that you DO NOT SELF-HOST any of our platform, but instead use the hosted (and attractively-priced) [Digital Growth Charts API platform](https://dev.rcpch.ac.uk/). Self-hosting means your organisation is fully liable for any errors in calculation, deployment, or functioning. We will not provide any free support for self-hosting organisations.**