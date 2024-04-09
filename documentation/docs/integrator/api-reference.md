---
title: API Reference
reviewers: Dr Marcus Baw, Dr Simon Chapman, Dr Anchit Chandran
audience: integrators, implementers, technical-architects
---
# API Reference

<!-- Embeds the Swagger UI view of the API reference here -->
<link type="text/css" rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">

<div id="swagger-ui"></div>

<script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js" charset="UTF-8"></script>

<script>
    const ui = SwaggerUIBundle({
    url: 'https://raw.githubusercontent.com/rcpch/digital-growth-charts-server/live/openapi.json',
    dom_id: '#swagger-ui',
    })
</script>
