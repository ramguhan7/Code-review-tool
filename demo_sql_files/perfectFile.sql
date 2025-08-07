SELECT
      CAST(TRIM(pop.API_OBJ_ID) AS DECIMAL(38, 0)) AS APIObjectID
    , CAST(TRIM(pop.DIST_SEQ_NBR) AS DECIMAL(38, 0)) AS DistributionSequenceNBR
    , CAST(TRIM(pop.COMPANY) AS DECIMAL(38, 0)) AS CompanyID
    , TRIM(b1.R_NAME) AS CompanyNM
    , TRIM(pop.VENDOR) AS VendorID
    , pop.INVOICE AS InvoiceID
    , CAST(TRIM(pop.SUFFIX) AS DECIMAL(38, 0)) AS SuffixID
    , CAST(TRIM(pop.CANCEL_SEQ) AS DECIMAL(38, 0)) AS CancelSEQ
    , CAST(TRIM(pop.ORIG_DIST_SEQ) AS DECIMAL(38, 0)) AS OriginalDistributionSEQ
    , TRIM(pop.DIST_TYPE) AS DistributionTypeCD
    , TRIM(pop.PROC_LEVEL) AS ProcessLevelCD
    , TRIM(pop.POST_OPTION) AS PostOptionCD
    , TRIM(pop.INVOICE_TYPE) AS InvoiceTypeCD
    , CAST(TRIM(pop.REC_STATUS) AS DECIMAL(38, 0)) AS RecordStatusCD
    , TRIM(pop.INV_CURRENCY) AS InvoiceCurrencyCD
    , CAST(TRIM(pop.TAX_RATE) AS DECIMAL(38, 7)) AS TaxRateNBR
    , CAST(TRIM(pop.CURR_RATE) AS DECIMAL(38, 7)) AS CurrencyExchangeNBR
    , CAST(TRIM(pop.ORIG_BASE_AMT) AS DECIMAL(38, 4)) AS OriginalBaseAMT
    , CAST(TRIM(pop.BASE_ND) AS DECIMAL(38, 0)) AS BaseDecimalPlacesNBR
    , CAST(TRIM(pop.ORIG_TRAN_AMT) AS DECIMAL(38, 4)) AS OriginalTransactionAMT
    , CAST(TRIM(pop.TRAN_ND) AS DECIMAL(38, 0)) AS TransactionDecimalPlacesNBR
    , CAST(TRIM(pop.TO_BASE_AMT) AS DECIMAL(38, 4)) AS ToCompanyBaseAMT
    , CAST(TRIM(pop.TO_BASE_ND) AS DECIMAL(38, 0)) AS ToCompanyBaseDecimalPlacesNBR
    , CAST(TRIM(pop.TAXABLE_AMT) AS DECIMAL(38, 4)) AS TaxableAMT
    , CAST(TRIM(pop.UNT_AMOUNT) AS DECIMAL(38, 4)) AS UnitAMT
    , CAST(TRIM(pop.DIST_COMPANY) AS DECIMAL(38, 0)) AS DistributionCompanyID
    , TRIM(b2.R_NAME) AS DistributionCompanyNM
    , TRIM(pop.DIS_ACCT_UNIT) AS AccountingUnitCD
    , TRIM(d.DESCRIPTION) AS AccountingUnitDSC
    , CAST(TRIM(pop.DIS_ACCOUNT) AS DECIMAL(38, 0)) AS AccountNBR
    , CAST(TRIM(pop.DIS_SUB_ACCT) AS DECIMAL(38, 0)) AS SubAccountNBR
    , pop.DISTRIB_DATE AS DistributionDTS
    , TRIM(pop.TAX_INDICATOR) AS TaxIndicatorCD
    , CAST(TRIM(pop.TAX_SEQ_NBR) AS DECIMAL(38, 0)) AS TaxSequenceNBR
    , TRIM(pop.TAX_CODE) AS TaxCD
    , TRIM(pop.TAX_TYPE) AS TaxTypeCD
    , TRIM(pop.DESCRIPTION) AS DistributionDSC
    , TRIM(pop.DST_REFERENCE) AS ReferenceNBR
    , TRIM(pop.ACTIVITY) AS ActivityCD
    , TRIM(a.DESCRIPTION) AS ActivityDSC
    , TRIM(pop.ACCT_CATEGORY) AS AccountCategoryCD
    , TRIM(pop.ACCR_CODE) AS InvoiceAccrualCD
    , TRIM(pop.PO_NUMBER) AS PONBR
    , CAST(TRIM(pop.PO_RELEASE) AS DECIMAL(38, 0)) AS POReleaseNBR
    , TRIM(pop.PO_CODE) AS POCD
    , CAST(TRIM(pop.PO_LINE_NBR) AS DECIMAL(38, 0)) AS POLineNBR
    , TRIM(pop.PO_AOC_CODE) AS POAddOnCostFLG
    , CAST(TRIM(pop.GLT_OBJ_ID) AS DECIMAL(38, 0)) AS GLObjectID
    , CAST(TRIM(pop.ATN_OBJ_ID) AS DECIMAL(38, 0)) AS ActivityObjectID
    , TRIM(pop.ASSET_FLAG) AS AssetCD
    , TRIM(pop.DIST_CODE) AS DistributionCD
    , TRIM(pop.TAX_POINT) AS TaxPointCD
    , CAST(TRIM(pop.DST_OBJ_ID) AS DECIMAL(38, 0)) AS DistributionObjectID
    , TRIM(pop.MA_CREATE_FL) AS MatchingCreationCD
    , CAST(TRIM(pop.AC_UPD_STATUS) AS DECIMAL(38, 0)) AS AccountUpdateStatusCD
    , pop.AC_UPD_DATE AS AccountUpdateDTS
    , CAST(TRIM(pop.AC_UPD_TIME) AS DECIMAL(38, 0)) AS AccountUpdateTimeNBR
    , TRIM(pop.DIVERSE_CODE) AS DiverseCD
    , CAST(TRIM(pop.DISTRIB_ADJ) AS DECIMAL(38, 0)) AS AdjustmentFLG
    , CAST(TRIM(pop.WEIGHT) AS DECIMAL(38, 4)) AS ItemWeightNBR
    , CAST(TRIM(pop.SUPLMNTARY_QTY) AS DECIMAL(38, 4)) AS SupplementaryCNT
    , TRIM(pop.PROD_TAX_CAT) AS ProductTaxCategoryCD
    , TRIM(pop.APDSET10_SS_SW) AS InvoiceDistributionSet10CD
    , TRIM(pop.APDSET11_SS_SW) AS InvoiceDistributionSet11CD
    , TRIM(pop.APDSET12_SS_SW) AS InvoiceDistributionSet12CD
    , TRIM(pop.APDSET5_SS_SW) AS InvoiceDistributionSet05CD
    , TRIM(pop.APDSET6_SS_SW) AS InvoiceDistributionSet06CD
    , TRIM(pop.APDSET8_SS_SW) AS InvoiceDistributionSet08CD
    , TRIM(pop.APDSET9_SS_SW) AS InvoiceDistributionSet09CD
    , TRIM(pop.L_ATAPD_SS_SW) AS LATAPDSubsetSWFLG
    , pop.LAST_UPDT_DATE AS LastUpdateDTS
FROM
    {{source_data}}.lawson.apdistrib AS pop
    LEFT JOIN {{source_data}}.lawson.APCOMPANY AS b1
        ON pop.COMPANY = b1.COMPANY
    LEFT JOIN {{source_data}}.lawson.APCOMPANY b2
        ON pop.COMPANY = b2.COMPANY
    LEFT JOIN {{source_data}}.lawson.GLNAMES d
        ON pop.DIS_ACCT_UNIT = d.ACCT_UNIT
        AND pop.COMPANY = d.COMPANY
    LEFT JOIN shca_source_data.lawson.acactivity AS a
        ON pop.ACTIVITY = a.activity --dont need this join 
;
