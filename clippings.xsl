<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<xsl:template match="/">
  <html>
    <body>
      <xsl:for-each select="root/item">
        <br/>
        <h1><xsl:value-of select="Title"/></h1>
          <ul>
            <xsl:for-each select="Quotes/item">
              <li>
                <xsl:value-of select="."/>
              </li>
            </xsl:for-each>
          </ul>
      </xsl:for-each>
    </body>
  </html>
</xsl:template>

</xsl:stylesheet>