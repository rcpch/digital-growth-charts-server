Option Private Module    'to keep functions not be shown in Excel function lists
Option Explicit
'7/7/2003
Declare Function WNetGetUser Lib "mpr.dll" _
      Alias "WNetGetUserA" (ByVal lpName As String, _
      ByVal lpUserName As String, lpnLength As Long) As Long

Public Const NoError = 0       'The Function call was successful 7/7/2003
Public PS As String, M As Object  'PS = "\" in Windows
Public pt As String   '1/3/2002
'for cal SDS
Public Const TXTCOMP As Integer = 1  'text comparison
Public Const STREQUAL As Integer = 0  'StrComp: equality
'frmWtGain
Public idxSex_g As Integer
Public idxAge1_g As Integer
Public idxAge2_g As Integer
Public idxSc1_g As Integer
Public idxSc2_g As Integer
Public idxSc1_g_o As Integer    '30/5/2003 for onechild
Public idxSc2_g_o As Integer    '30/5/2003 for onechild
Public idxWT1_g As Integer
Public idxWT2_g As Integer
Public idxSDS_g As Integer
Public DatRow1_g As Long
Public DatRow2_g As Long
Public NHead_g As Integer       '31/1/2005
Public ColName(256) As String  '*2?
Public AgeScale(4) As String
Public DataFile As String       'default "British1990.xls"
Public RfPath As String         'reference path ...\XLSTART
Public RfFiles() As String       'reference file names
Public RfCurIndex As Integer     'index of the current reference
'Public RfDefIndex As Integer    'index for the default reference
Public RfTotal As Integer        'total number of references
Public Const MaxN As Integer = 6  'max number of measures to be selected for one reference
Public Const MaxM As Integer = 6  'max length for label title of measurement and time
Public NameTotal As Integer       'total names in reference
Public NameUsed As Integer        'if NameTotal> 6 then NameUsed = 6 else NameUsed = NameTotal
Public tName As String            'name of time
Public mName() As String          'names of measurement in reference data
Public tTitle As String           'title for time
Public mTitle() As String         'title for measurement
Public tUnit As String            'unit for age
Public mUnit() As String          'unit for measurement
'for frmSDSFx of SDS & centiles
Public idxSex_s As Integer
Public idxAge_s As Integer          'when use Age
Public idxAgeD_s As Integer         'when use Dates to produce Age  21/1/2005
Public idxM1_s(6) As Integer
Public idxM2_s(6) As Integer
Public idxM3_s(6) As Integer
Public Datetype_s As Integer         '1-dates, 0-age as defaule frmSDSfx 1/12/2004
Public idxGest_s As Integer          '1/12/2004
Public idxBirth_s As Integer         '1/12/2004
Public idxMeaDate_s As Integer       '1/12/2004 date at measure
Public idxStoM_s As Integer          '7/1/2005, 1-to Mea, 0-to SDS
Public idxCov1_s As Integer          '21/5/2007 for covariates
Public idxCov2_s As Integer          '21/5/2007
Public DaRow1_s As Long
Public DaRow2_s As Long
Public NHead_s As Integer            '12/1/2005, 1-with head
Public SaUnit As Integer             '19/5/2003 index for the user age unit of calc SDS 1-yr,2-mo,3-wk,4-dy
'for frmSDSCov for SDS with covariates   '20/6/2007
Public idxSex_c As Integer
Public idxAge_c As Integer          'Age
Public idxAgeD_c As Integer         'Dates to produce Age
Public idxM1_c(6) As Integer
Public idxM2_c(6) As Integer
Public idxM3_c(6) As Integer
Public Datetype_c As Integer         '1-dates, 0-age as defaule frmSDSfx
Public idxGest_c As Integer
Public idxBirth_c As Integer
Public idxMeaDate_c As Integer       'date at measure
Public idxStoM_c As Integer          '1-to Mea, 0-to SDS
Public idxCov1_c As Integer          'covariates
Public idxCov2_c As Integer          '
Public DaRow1_c As Long
Public DaRow2_c As Long
Public NHead_c As Integer            '1-with head
Public CaUnit As Integer    'age unit for cov ref
Public NumCov As Integer    '15/5/2007 number of covariates
Public Cov1Title As String   '15/5/2007 name of covariates
Public Cov2Title As String   '15/5/2007 name of covariates
Public Cov1Lab As String     '25/7/2007 label of covariates
Public Cov2Lab As String     '25/7/2007 label of covariates
Public cov1 As Single       '15/5/2007  covariate for onechild & SDSCov
Public cov2 As Single       '15/5/2007  covariate for onechild & SDSCov
Public Fidx As Integer      '21/6/2007
Public FNClist() As String  '21/6/2007
Public Fidx_c As Integer    '22/6/2007 in frmSDSCov
Public Fidx_s As Integer    '24/7/2007 in frmSDSFx
'for frmIOTF of IOTF
Public idxSex_I As Integer
Public idxAge_I As Integer
Public idxM1_I As Integer
Public idxM2_I As Integer
Public idxWt_I As Integer            '11/8/2005
Public idxHt_I As Integer            '11/8/2005
Public idxWH_I As Integer            '15/8/2005
Public NuseWH_I As Integer           '11/8/2005 1-Wt & Ht, 0-BMI
Public DaRow1_I As Long
Public DaRow2_I As Long
Public NHead_I As Integer            '28/1/2005
Public IaUnit As Integer   '2/7/2003 index for the user age unit of calc IOTF 1-yr,2-mo,3-wk,4-dy
Public IaUnit_o As Integer '3/7/2003 index for the user age unit of calc IOTF 1-yr,2-mo,3-wk,4-dy
'global
Public HWB() As Integer         'ht, wt, bmi,head, sitht, legln's position
Public invHWB() As Integer      'index of position to ht,wt,bmi,head,sitht & legln  17/8/2005
Public OkHWB As Integer    'if y_weight_kg, y_height_cm & y_BMI_kgm2 exist in Ref data
Public OKHSL As Integer    'if y_height_cm & y_sitht_cm & y_legln_cm exist in Ref data 16/8/2005
Public OkWT As Integer     '14/4/2003  if name of weight_kg exists
Public WTat As Integer     '14/4/2003  the order number of weight name in reference
Public NOpenRf As Integer  '15/5/2003  NOpenRf = 0 when start, >=1 once call getExistingXY
Public OkAge As Integer    '16/5/2003 if age unit for yr,year,years,mo, month, months,wk,week,weeks,dy,day,days
Public CPU As String * 3   '22/5/2003 for operatingSystem
Public ZoomSize As Single  '22/5/2003 100 for PC, 100*100/75 for Mac
Public Const ZoomPC As Single = 100
Public Const ZoomMac As Single = 100    '100 * 100 / 75
Public Const txtHtMac As Single = 1.2   '10/6/2003
Public Const unknown As String = "N/A"   '22/5/2003
'Public Const Zcutoff As Integer = 8      '23/5/2003 for SDS, remove 6/3/2009
Public Const Mcutoff As Integer = 0      '23/5/2003 for measurements
Public PathRoot As String                '2/6/2003
Public IOTFRf(33, 4) As Single           '0-t, 1-boy overwt, 2-boy obesity, 2-girl overwt, 4-girl obesity
Public IOTFm(33, 5) As Single            '0-t,1-16,2-17,3-18.5,4-25,5-30 for male 20/4/2007
Public IOTFf(33, 5) As Single            '0-t,1-16,2-17,3-18.5,4-25,5-30 for female 20/4/2007
Public SaveFname As String                '=PathRoot & "Growth" & Application.UserName
Public Const unknown2 As String = ""     '10/9/2004
Public DefXYname() As String             '25/11/2004 for names of British1990
Public Const DefNoname As Integer = 9    'total valid name in British1990 for VBA use is 8 (>6 shown in dialog), 4/2/2011 fat added
Public DefSpiroNm() As String            '2/8/2007 manually range sequence of names of Sprio
Public Const DefNoSpiro As Integer = 7   'total valid name in Spiro.xls, 18/12/2008 5->7
'frmZP  13/12/2004
Public Const Ncentmax = 30  '14/12/2004 copy from LMS
Public Const Ncentmin = 1
Public Const Ncentadj = 31  'Ncentmax+Ncentmin
Public sdscent() As Single
Public pcent(30) As Single
Public scent(30) As Single
Public NcentU As Integer
Public Ncent As Integer
Public porz As Integer      '1-percentile, 2-Z of GrdUequal
Public nequal As Integer
Public NcentE As Integer
Public space As Single      '8/2/2005 double->single
Public Puequal As String     '16/5/2005 for txtP of frmZP
Public Zuequal As String       '16/6/2005 for txtZ of frmZP
Public idxSex_zp As Integer
Public idxAge_zp As Integer
Public idxOut_zp As Integer
Public idxMea_zp As Integer
Public DaRow1_zp As Integer
Public DaRow2_zp As Integer
Public idxFor_zp As Integer
Public idxTo_zp As Integer
'Public AgeR_zp As String
Public ta As Single      'min of the real age
Public tz As Single      'max of the real age
Public tint As Single
Public tnumber As Long
Public nstart As Long
Public OaUnit As Integer    '17/1/2005   age unit in frmOneChild
Public DataRef As String    '17/5/2005   e.g. British1990
Public idxDec_P As Integer  '29/11/2005 for decimals of sds output in frmPref,  '9/11/2007 remove, keep for tmp 27/5/2009
'Public NAgree As Integer    '12/5/2006, 21/8/2008 remove
Public Wname As String      '9/12/2006
Public NewRf As Integer     '1-create new ref
Public Const MacHelp1 As String = "For Help with LMSgrowth for Mac,"   '3/5/2007
Public Const MacHelp2 As String = "please see the documentation in LMSgrowth.PDF  "   '3/5/2007
Public Const MacHelp3 As String = "that came with the program."   '3/5/2007
Public zLLN(6) As Single           '21/3/2011
Public pLLN(6) As String           '25/3/2011, 30/3/2011 single->string
Public ppLLN(6) As String          '5/4/2011 for cobLLN display
Public idxLLN As Integer           '25/3/2011, 1-6, 6 for the 5th centile
Public idxOneChildCov As Integer   '4/4/2011
Public idxOneChildFx As Integer    '5/4/2011
Public idxSDSCov As Integer        '5/4/2011
Public idxSDSFx As Integer         '5/4/2011
' Key Codes
Global Const KEY_LBUTTON = &H1
Global Const KEY_RBUTTON = &H2
Global Const KEY_CANCEL = &H3
Global Const KEY_MBUTTON = &H4    ' NOT contiguous with L & RBUTTON
Global Const KEY_BACK = &H8
Global Const KEY_TAB = &H9
Global Const KEY_CLEAR = &HC
Global Const KEY_RETURN = &HD
Global Const KEY_SHIFT = &H10
Global Const KEY_CONTROL = &H11
Global Const KEY_MENU = &H12
Global Const KEY_PAUSE = &H13
Global Const KEY_CAPITAL = &H14
Global Const KEY_ESCAPE = &H1B
Global Const KEY_SPACE = &H20
Global Const KEY_PRIOR = &H21
Global Const KEY_NEXT = &H22
Global Const KEY_END = &H23
Global Const KEY_HOME = &H24
Global Const KEY_LEFT = &H25
Global Const KEY_UP = &H26
Global Const KEY_RIGHT = &H27
Global Const KEY_DOWN = &H28
Global Const KEY_SELECT = &H29
Global Const KEY_PRINT = &H2A
Global Const KEY_EXECUTE = &H2B
Global Const KEY_SNAPSHOT = &H2C
Global Const KEY_INSERT = &H2D
Global Const KEY_DELETE = &H2E
Global Const KEY_HELP = &H2F
'Zorder method
Global Const BRINGTOFRONT = 0
Global Const SENDTOBACK = 1
'HTML help 1/4/2011
Const HH_DISPLAY_TOPIC = &H0
Const HH_HELP_CONTEXT = &HF         ' Display mapped numeric value in  dwData.
Declare Function HtmlHelp Lib "hhctrl.ocx" Alias "HtmlHelpA" (ByVal hwndCaller As Long, ByVal pszFile As String, ByVal uCommand As Long, ByVal dwData As Long) As Long







Sub CalcLegnew(indexHT As Integer, indexsitht As Integer, indexlegln As Integer, indexHead As Integer, row1 As Long, row2 As Long)
'17/8/2005 for leg =ht-st automatic calc
Dim i As Long, cur As String, j1 As Integer, j2 As Integer, tmprow1 As Long
On Error GoTo E
Application.ScreenUpdating = False

cur = ColName(indexlegln)
j1 = indexHT - indexlegln
j2 = indexsitht - indexlegln
If indexHead = 1 Then  'for *_I & *_S
   tmprow1 = row1 + 1
   Range(cur & row1).value = "Legln"
Else
   tmprow1 = row1
End If
For i = tmprow1 To row2   '13/7/2005
    Range(cur & i).Select
    ActiveCell.FormulaR1C1 = "=Legnew(RC[" & j1 & "],RC[" & j2 & "])"
Next i
Application.ScreenUpdating = True
Exit Sub
E:
'MsgBox ("Problem in CalcBMI"), 48, "LMSgrowth"  '10/9/2004 remove

End Sub

Function cCent(sexRange As Variant, tRange As Variant, DAgeU As String, Yrange As Variant, agname As String, meaName As String, Dfile As String) As Variant
'13/12/2005 copy from cCentile, change unknown -> unknown2 for frmZP
Dim LL As Single, MM As Single, SS As Single, tmin As Single, tmax As Single
Dim cols As Integer, t As Single, Y As Single, AgeCol As String, MeaCol As String
Dim k As Long, ScrFail As Integer, DataAgeCol As String, DataMeaCol As String
Dim AgeR As Single, RAgeU As String, Nm As Integer   '8/3/2005
Dim LSY As Single    '27/5/2009

'On Error Resume Next
On Error GoTo E
cCent = unknown2    'unknown -> unknown2 on 13/12/2005
AgeCol = agname     '29/11/2004
MeaCol = meaName    '17/11/2004
'check reference
If IsBookOpen(Dfile) = False Then
   If Not IsDiskFile(Dfile) Then
      Exit Function
   Else
      Workbooks.Open Dfile  'was in Sub Binarysearch
   End If
End If
If IsNameExist(AgeCol, Dfile) = False Then
   Exit Function
End If
If IsNameExist(MeaCol, Dfile) = False Then
   Exit Function
End If
DataAgeCol = Dfile & "!" & AgeCol
DataMeaCol = Dfile & "!" & MeaCol
    'check sex
    If IsMissing(sexRange) = True Then GoTo E
    If sexRange = "" Then GoTo E
    If (Not IsNumeric(sexRange)) Then
        'If sexRange = "M" Or sexRange = "m" Then
        If UCase(Trim(sexRange)) = "M" Or UCase(Trim(sexRange)) = "MALE" Then   '17/8/2005
           cols = 3
        Else
          'If sexRange = "F" Or sexRange = "f" Then
           If UCase(Trim(sexRange)) = "F" Or UCase(Trim(sexRange)) = "FEMALE" Then   '17/8/2005
             cols = 6
          Else
             GoTo E
          End If
        End If
    Else
       If sexRange = 1 Then
          cols = 3
       Else
          If sexRange = 2 Then
             cols = 6
          Else
             GoTo E
          End If
       End If
    End If
    'Check age
    If IsMissing(tRange) = True Then GoTo E
    If tRange = "" Then GoTo E
    If (Not IsNumeric(tRange)) Then GoTo E
    k = Range(DataAgeCol).Rows.Count
    tmin = Range(DataAgeCol).Rows(1)
    tmax = Range(DataAgeCol).Rows(k)
    'nm = InStrRev(AgeCol, "_")     'add 8/3/2005, remove as InStrRev not available in Mac
    Nm = RevSearch(AgeCol, "_")    '22/3/2005
    If Nm <> 0 Then RAgeU = Mid(AgeCol, Nm + 1, Len(AgeCol) - Nm) Else GoTo E '8/3/2005
    getAgeRate DAgeU, RAgeU, AgeR   '8/3/2005
    t = tRange * AgeR   '3/2/2005
    'If (t < -0.326) Or (t > 23) Then GoTo E
    If (t < tmin) Or (t > tmax) Then GoTo E
   'check yy
    If IsMissing(Yrange) Then GoTo E
    If Yrange = "" Then GoTo E
    If (Not IsNumeric(Yrange)) Then GoTo E

Y = Yrange
'If Abs(Y) >= Zcutoff Then GoTo E   'remove 6/3/2009
BinarySearch t, DataAgeCol, DataMeaCol, cols, LL, MM, SS, ScrFail
If ScrFail = 1 Then GoTo E
If LL = 1 Then
   cCent = 1 + SS * Y
Else
   If LL <> 0 Then
      LSY = LL * SS * Y     '27/5/2009
      If LSY > -1 Then     '27/5/2009
            cCent = (1 + LSY) ^ (1 / LL)
      Else
            GoTo E
      End If
      'cCent = (1 + LL * SS * Y) ^ (1 / LL) 'VBA's log = Excel's =Application.LN
   Else
      cCent = Exp(SS * Y)
   End If
End If
cCent = cCent * MM
'cCent = Format(cCent, "#######0.00")  'eg 12.295 -> 12.30  13/5/2003 treat as a string
'cCent = Round(cCent, 3)   'eg 12.295 -> 12.3  22/5/2003 Round function not available in Mac
cCent = Int(cCent * 1000 + 0.5) / 1000 '10/6/2003
Exit Function

E:
'MsgBox "problem in cCent", 48, "LMSgrowth"  'remove 10/9/2004
End Function


Sub ChkAgree(err As Integer)
''21/8/2008 remove, 12/5/2006 for License agreement
'Dim agname As String, s As String, FileNumber As Integer
'err = 0: NAgree = 0
'If CPU = "Mac" Then
'   NAgree = 1
'   Exit Sub  'as Dir does not work on Mac
'End If
'On Error GoTo E 'if British 1990 not available
'agname = PathRoot & "agree"
'If Len(Dir(agname)) = 0 Then
'   frmAgree.Show
'Else
'   NAgree = 1
'   Exit Sub
'End If
'If NAgree = 1 Then
'     On Error GoTo E    'use default British 1990
'     FileNumber = FreeFile
'     Open agname For Output As #FileNumber
'     s = "I agree the lincese."
'     Print #FileNumber, s
'     Close #FileNumber
'End If
'Exit Sub
'E:
'err = 1
End Sub



Sub CovAdd(Dfile As String, Rt As Long, CC As Integer, t As Single, cov1 As Single, cov2 As Single, LMS As Single)
'3/4/2007
On Error GoTo E
Dim loglink As Integer, logcov1 As Integer, logcov2 As Integer, s As String, powerT As Single, tmpcov1 As Single, tmpcov2 As Single, tmpt As Single
err = 0
s = Mid(Dfile, 1, Len(Dfile) - 4)
Select Case Rt
    Case 10  'one covariate
         loglink = Workbooks(Dfile).Sheets(s).Cells(Rt - 6, CC).value
         logcov1 = Workbooks(Dfile).Sheets(s).Cells(Rt - 5, CC).value
         powerT = Workbooks(Dfile).Sheets(s).Cells(Rt - 1, CC).value
         If logcov1 = 1 And cov1 > 0 Then tmpcov1 = Log(cov1) Else tmpcov1 = cov1
         If powerT = 0 Then tmpt = Log(t) Else tmpt = t ^ powerT
         LMS = Workbooks(Dfile).Sheets(s).Cells(Rt - 4, CC) + Workbooks(Dfile).Sheets(s).Cells(Rt - 3, CC) * tmpcov1 + Workbooks(Dfile).Sheets(s).Cells(Rt - 2, CC) * tmpt + LMS
    Case 12  'two covariates
         loglink = Workbooks(Dfile).Sheets(s).Cells(Rt - 8, CC).value
         logcov1 = Workbooks(Dfile).Sheets(s).Cells(Rt - 7, CC).value
         logcov2 = Workbooks(Dfile).Sheets(s).Cells(Rt - 6, CC).value
         powerT = Workbooks(Dfile).Sheets(s).Cells(Rt - 1, CC).value
         If logcov1 = 1 And cov1 > 0 Then tmpcov1 = Log(cov1) Else tmpcov1 = cov1
         If logcov2 = 1 And cov2 > 0 Then tmpcov2 = Log(cov2) Else tmpcov2 = cov2
         If powerT = 0 Then tmpt = Log(t) Else tmpt = t ^ powerT
         LMS = Workbooks(Dfile).Sheets(s).Cells(Rt - 5, CC) + Workbooks(Dfile).Sheets(s).Cells(Rt - 4, CC) * tmpcov1 + Workbooks(Dfile).Sheets(s).Cells(Rt - 3, CC) * tmpcov2 + Workbooks(Dfile).Sheets(s).Cells(Rt - 2, CC) * tmpt + LMS
End Select
If loglink = 1 Then LMS = Exp(LMS)
E:
loglink = loglink  'for test
End Sub

Sub FindFirstEmptyCol(col As Integer)
'31/3/2005
Dim LastCol As Integer
On Error GoTo E   'very important as empty sheet cause error
LastCol = ActiveSheet.Cells.Find(What:="*", SearchDirection:=xlPrevious, SearchOrder:=xlByColumns).Column
col = LastCol + 1
Exit Sub
E:
col = 1

'12/1/2005 wrote, 31/3/2005 remove as it treat blank cell with format as not blank
'Dim NUsed As Integer, Rused As Long, NCused As Long, CM As Integer, Cused As Long
'CM = Application.Calculation
'Application.Calculation = xlManual
'NUsed = ActiveSheet.UsedRange.Areas.Count
'Cused = ActiveSheet.UsedRange.Column
'NCused = ActiveSheet.UsedRange.Columns.Count
'If NUsed <> 0 Then col = Cused + NCused Else col = 1
'Application.Calculation = CM

End Sub


Sub CalcCentZP(iSex As Integer)
'23/12/2004
On Error GoTo E

Dim i As Integer
For i = 1 To Ncent
    CentYMWDzp i, iSex    '4/3/2005
Next i
E:

End Sub


Sub CentYMWDzp(idex As Integer, iSex As Integer)

'23/12/2004 idex from 1 to Ncent
Dim j2 As Integer, cur As String, tmpaName As String, tmpName As String, tmpDfile As String, tmpZ As String
Dim tmpDAgeU As String    '8/3/2005
On Error GoTo E

j2 = idxOut_zp - (idxOut_zp + idex)   '-idex
cur = ColName(idxOut_zp + idex) 'use 256 columns
Range(cur & 1).value = "Z=" & Format$(sdscent(idex), "#0.000")  'z title here, age title given in sub ChkAgeUnit in frmZP
Range(cur & DaRow1_zp).Select
tmpName = Chr(34) & mName(idxMea_zp + 1) & Chr(34)
tmpDfile = Chr(34) & DataFile & Chr(34)
tmpaName = Chr(34) & tName & Chr(34)
tmpZ = Chr(34) & Format$(sdscent(idex), "#0.000000") & Chr(34)  '6/12/2004
If idxAge_zp > 0 Then tmpDAgeU = Chr(34) & frmZP!cobAge.Text & Chr(34) Else tmpDAgeU = Chr(34) & tUnit & Chr(34)
Dim Ssex As Variant
Select Case iSex     '4/3/2005
   Case 0
        Ssex = Chr(34) & "M" & Chr(34)
   Case 1
        Ssex = Chr(34) & "F" & Chr(34)
End Select
ActiveCell.FormulaR1C1 = "=cCent(" & Ssex & ",RC[" & j2 & "]," & tmpDAgeU & "," & tmpZ & "," & tmpaName & ", " & tmpName & ", " & tmpDfile & ")"    '13/12/2005
If DaRow2_zp > DaRow1_zp Then
   Range(cur & DaRow1_zp).Select
   Selection.AutoFill Destination:=Range(cur & DaRow1_zp & ":" & cur & DaRow2_zp), Type:=xlFillDefault
End If

Exit Sub
E:
'MsgBox "Error in CentYMWD", 48, "LMSgrowth"  'remove 10/9/2004

End Sub




Sub FindUsedRows(row1 As Long, row2 As Long)

'31/3/2005

On Error GoTo E   'very important as empty sheet cause error
row2 = ActiveSheet.Cells.Find(What:="*", SearchDirection:=xlPrevious, SearchOrder:=xlByRows).Row
row1 = ActiveSheet.Cells.Find(What:="*", SearchDirection:=xlNext, SearchOrder:=xlByRows).Row

Exit Sub
E:
row1 = 0: row2 = 0

'12/1/2005, remove 31/3/2005 as somtimes not work well, eg empty cells with format are considered as not empty
'Dim NUsed As Integer, Rused As Long, NRUsed As Long, CM As Integer
''Dim NSel As Integer, RSel As Long, NRSel As Long, NCSel As Long, Ar As String  'remove 12/1/2005

'CM = Application.Calculation
'Application.Calculation = xlManual
''Ar = Selection.Address      'remove 12/1/2005 only consider used area not selected one
''NSel = Selection.Areas.Count
''RSel = Range(Ar).Row
''NRSel = Range(Ar).Rows.Count
'NCSel = Range(Ar).Columns.Count
'NUsed = ActiveSheet.UsedRange.Areas.Count
'Rused = ActiveSheet.UsedRange.Row
'NRUsed = ActiveSheet.UsedRange.Rows.Count
'Application.Calculation = CM
'If NUsed <> 0 Then
   'row1 = Rused
   'row2 = Rused + NRUsed - 1
'Else
   'row1 = 0: row2 = 0
'End If

End Sub

Sub getAgeRate(DAgeU As String, RAgeU As String, rate As Single)
'7/3/2005 to replace CalcAgeRate
'17/11/2004 copy the age scale change from centYMWD1 and edit it

Select Case DAgeU 'data age unit
  Case "yr", "year", "years"
      Select Case RAgeU 'Ref age unit
        Case "yr", "year", "years"
            rate = 1
        Case "mo", "month", "months"
            rate = 12
        Case "wk", "week", "weeks"
            rate = 365.25 / 7
        Case "dy", "day", "days"
            rate = 365.25
      End Select
  Case "mo", "month", "months"   'mo for data age unit
      Select Case RAgeU  'Ref age unit
        Case "yr", "year", "years"
            rate = 1 / 12
        Case "mo", "month", "months"
            rate = 1
        Case "wk", "week", "weeks"
            rate = 365.25 / 84
        Case "dy", "day", "days"
            rate = 365.25 / 12
      End Select
   Case "wk", "week", "weeks" 'wk for data age unit
      Select Case RAgeU  'Ref age unit
        Case "yr", "year", "years"
            rate = 7 / 365.25
        Case "mo", "month", "months"
            rate = 84 / 365.25
        Case "wk", "week", "weeks"
            rate = 1
        Case "dy", "day", "days"
            rate = 7
      End Select
   Case "dy", "day", "days"  'dy for data age unit
      Select Case RAgeU  'Ref age unit
        Case "yr", "year", "years"
            rate = 1 / 365.25
        Case "mo", "month", "months"
            rate = 12 / 365.25
        Case "wk", "week", "weeks"
            rate = 1 / 7
        Case "dy", "day", "days"
            rate = 1
      End Select
   Case Else
      rate = 1
End Select
End Sub






Sub CalcAgeRate(dataUnit As Integer, rate As String)
'17/11/2004 copy the age scale change from centYMWD1 and edit it

Select Case dataUnit 'data age unit
  Case 0 'no change as ref age unit
       rate = "1"
  Case 1  'yr for data age unit
      Select Case tUnit 'Ref age unit
        Case "yr", "year", "years"
            rate = "1"
        Case "mo", "month", "months"
            rate = "12"
        Case "wk", "week", "weeks"
            rate = "365.25/7"
        Case "dy", "day", "days"
            rate = "365.25"
      End Select
  Case 2 'mo for data age unit
      Select Case tUnit  'Ref age unit
        Case "yr", "year", "years"
            rate = "1/12"
        Case "mo", "month", "months"
            rate = "1"
        Case "wk", "week", "weeks"
            rate = "365.25/84"
        Case "dy", "day", "days"
            rate = "365.25/12"
      End Select
   Case 3 'wk for data age unit
      Select Case tUnit  'Ref age unit
        Case "yr", "year", "years"
            rate = "7/365.25"
        Case "mo", "month", "months"
            rate = "84/365.25"
        Case "wk", "week", "weeks"
            rate = "1"
        Case "dy", "day", "days"
            rate = "7"
      End Select
   Case 4 'dy for data age unit
      Select Case tUnit  'Ref age unit
        Case "yr", "year", "years"
            rate = "1/365.25"
        Case "mo", "month", "months"
            rate = "12/365.25"
        Case "wk", "week", "weeks"
            rate = "1/7"
        Case "dy", "day", "days"
            rate = "1"
      End Select
End Select
End Sub
Function cCentile(sexRange As Variant, tRange As Variant, DAgeU As String, Yrange As Variant, agname As String, meaName As String, Dfile As String) As Variant

Dim LL As Single, MM As Single, SS As Single, tmin As Single, tmax As Single
Dim cols As Integer, t As Single, Y As Single, AgeCol As String, MeaCol As String
Dim k As Long, ScrFail As Integer, DataAgeCol As String, DataMeaCol As String
Dim AgeR As Single, RAgeU As String, Nm As Integer   '8/3/2005
Dim LSY As Single    '27/5/2009

'On Error Resume Next
On Error GoTo E
cCentile = unknown    '10/9/2004
AgeCol = agname     '29/11/2004
MeaCol = meaName    '17/11/2004
'check reference
If IsBookOpen(Dfile) = False Then
   If Not IsDiskFile(Dfile) Then
      Exit Function
   Else
      Workbooks.Open Dfile  'was in Sub Binarysearch
   End If
End If
If IsNameExist(AgeCol, Dfile) = False Then
   Exit Function
End If
If IsNameExist(MeaCol, Dfile) = False Then
   Exit Function
End If
DataAgeCol = Dfile & "!" & AgeCol
DataMeaCol = Dfile & "!" & MeaCol
    'check sex
    If IsMissing(sexRange) = True Then GoTo E
    If sexRange = "" Then GoTo E
    If (Not IsNumeric(sexRange)) Then
        If UCase(Trim(sexRange)) = "M" Or UCase(Trim(sexRange)) = "MALE" Then   '17/8/2005
           cols = 3
        Else
           If UCase(Trim(sexRange)) = "F" Or UCase(Trim(sexRange)) = "FEMALE" Then   '17/8/2005
             cols = 6
          Else
             GoTo E
          End If
        End If
    Else
       If sexRange = 1 Then
          cols = 3
       Else
          If sexRange = 2 Then
             cols = 6
          Else
             GoTo E
          End If
       End If
    End If
    'Check age
    If IsMissing(tRange) = True Then GoTo E
    If tRange = "" Then GoTo E
    If (Not IsNumeric(tRange)) Then GoTo E
    k = Range(DataAgeCol).Rows.Count
    tmin = Range(DataAgeCol).Rows(1)
    tmax = Range(DataAgeCol).Rows(k)
    'nm = InStrRev(AgeCol, "_")     'add 8/3/2005, remove as InStrRev not available in Mac
    Nm = RevSearch(AgeCol, "_")    '22/3/2005
    If Nm <> 0 Then RAgeU = Mid(AgeCol, Nm + 1, Len(AgeCol) - Nm) Else GoTo E '8/3/2005
    getAgeRate DAgeU, RAgeU, AgeR   '8/3/2005
    t = tRange * AgeR   '3/2/2005
    'If (t < -0.326) Or (t > 23) Then GoTo E
    If (t < tmin) Or (t > tmax) Then GoTo E
   'check yy
    If IsMissing(Yrange) Then GoTo E
    If Yrange = "" Then GoTo E
    If (Not IsNumeric(Yrange)) Then GoTo E

Y = Yrange
'If Abs(Y) >= Zcutoff Then GoTo E   'remove 6/3/2009
BinarySearch t, DataAgeCol, DataMeaCol, cols, LL, MM, SS, ScrFail
If ScrFail = 1 Then GoTo E
If LL = 1 Then
   cCentile = 1 + SS * Y
Else
   If LL <> 0 Then
      LSY = LL * SS * Y     '27/5/2009
      If LSY > -1 Then     '27/5/2009
            cCentile = (1 + LSY) ^ (1 / LL)
      Else
            GoTo E
      End If
      'cCentile = (1 + LL * SS * Y) ^ (1 / LL) 'VBA's log = Excel's =Application.LN
   Else
      cCentile = Exp(SS * Y)
   End If
End If
cCentile = cCentile * MM
'cCentile = Format(cCentile, "#######0.00")  'eg 12.295 -> 12.30  13/5/2003 treat as a string
'cCentile = Round(cCentile, 3)   'eg 12.295 -> 12.3  22/5/2003 Round function not available in Mac
cCentile = Int(cCentile * 1000 + 0.5) / 1000 '10/6/2003
Exit Function

E:
'MsgBox "problem in cCentile", 48, "LMSgrowth"  'remove 10/9/2004
End Function
Function cCentileg(sexRange As Variant, gRange As Variant, tRange As Variant, DAgeU As String, Yrange As Variant, agname As String, meaName As String, Dfile As String) As Variant
'24/1/2005 modify cCentile for gestation
Dim LL As Single, MM As Single, SS As Single, tmin As Single, tmax As Single
Dim cols As Integer, t As Single, Y As Single, AgeCol As String, MeaCol As String, gt As Single
Dim k As Long, ScrFail As Integer, DataAgeCol As String, DataMeaCol As String
Dim AgeR As Single, RAgeU As String, Nm As Integer   '8/3/2005
Dim LSY As Single    '27/5/2009

'On Error Resume Next
On Error GoTo E
cCentileg = unknown    '10/9/2004
AgeCol = agname     '29/11/2004
MeaCol = meaName    '17/11/2004

'check reference
If IsBookOpen(Dfile) = False Then
   If Not IsDiskFile(Dfile) Then
      Exit Function
   Else
      Workbooks.Open Dfile  'was in Sub Binarysearch
   End If
End If
If IsNameExist(AgeCol, Dfile) = False Then
   Exit Function
End If
If IsNameExist(MeaCol, Dfile) = False Then
   Exit Function
End If
DataAgeCol = Dfile & "!" & AgeCol
DataMeaCol = Dfile & "!" & MeaCol
    'check sex
    If IsMissing(sexRange) = True Then GoTo E
    If sexRange = "" Then GoTo E
    If (Not IsNumeric(sexRange)) Then
        If UCase(Trim(sexRange)) = "M" Or UCase(Trim(sexRange)) = "MALE" Then   '17/8/2005
           cols = 3
        Else
          If UCase(Trim(sexRange)) = "F" Or UCase(Trim(sexRange)) = "FEMALE" Then   '17/8/2005
             cols = 6
          Else
             GoTo E
          End If
        End If
    Else
       If sexRange = 1 Then
          cols = 3
       Else
          If sexRange = 2 Then
             cols = 6
          Else
             GoTo E
          End If
       End If
    End If
    'Check age
    If IsMissing(tRange) = True Then GoTo E
    If tRange = "" Then GoTo E
    If (Not IsNumeric(tRange)) Then GoTo E
    If IsMissing(gRange) = True Then GoTo E
    If gRange = "" Then GoTo E
    If (Not IsNumeric(gRange)) Then GoTo E
    k = Range(DataAgeCol).Rows.Count
    tmin = Range(DataAgeCol).Rows(1)
    tmax = Range(DataAgeCol).Rows(k)
    gt = gRange
    'nm = InStrRev(AgeCol, "_")     '8/3/2005,  remove as InStrRev not available in Mac
    Nm = RevSearch(AgeCol, "_")    '22/3/2005
    If Nm <> 0 Then RAgeU = Mid(AgeCol, Nm + 1, Len(AgeCol) - Nm) Else GoTo E '8/3/2005
    getAgeRate DAgeU, RAgeU, AgeR   '8/3/2005
    t = tRange * AgeR  '3/2/2005
    'Select Case agUnit    'gRang in wk
    Select Case RAgeU    '8/3/2005
         Case "yr", "year", "years"
               t = t - (40 - gt) * 7 / 365.25
         Case "mo", "month", "months"
               t = t - (40 - gt) * 84 / 365.25
         Case "wk", "week", "weeks"
               t = t - (40 - gt)
         Case "dy", "day", "days"
               t = t - (40 - gt) * 7
         Case Else
              GoTo E
   End Select
   'If (t < -0.326) Or (t > 23) Then GoTo E
   If (t < tmin) Or (t > tmax) Then GoTo E

   'check yy
    If IsMissing(Yrange) Then GoTo E
    If Yrange = "" Then GoTo E
    If (Not IsNumeric(Yrange)) Then GoTo E

Y = Yrange
'If Abs(Y) >= Zcutoff Then GoTo E   'remove 6/3/2009
BinarySearch t, DataAgeCol, DataMeaCol, cols, LL, MM, SS, ScrFail
If ScrFail = 1 Then GoTo E
If LL = 1 Then
   cCentileg = 1 + SS * Y
Else
   If LL <> 0 Then
      LSY = LL * SS * Y     '27/5/2009
      If LSY > -1 Then     '27/5/2009
            cCentileg = (1 + LSY) ^ (1 / LL)
      Else
            GoTo E
      End If
      'cCentileg = (1 + LL * SS * Y) ^ (1 / LL) 'VBA's log = Excel's =Application.LN
   Else
      cCentileg = Exp(SS * Y)
   End If
End If
cCentileg = cCentileg * MM
'cCentileg = Format(cCentileg, "#######0.00")  'eg 12.295 -> 12.30  13/5/2003 treat as a string
'cCentileg = Round(cCentileg, 3)   'eg 12.295 -> 12.3  22/5/2003 Round function not available in Mac
cCentileg = Int(cCentileg * 1000 + 0.5) / 1000 '10/6/2003
Exit Function

E:
'MsgBox "problem in cCentileg", 48, "LMSgrowth"  'remove 10/9/2004
End Function






Sub CentYMWD(idex As Integer, iSex As Integer)
'17/11/2004 modify, 24/1/2005 modify for head
Dim j1 As Integer, j2 As Integer, j3 As Integer, j4 As Integer, cur As String, tmpaName As String, tmpName As String, tmpDfile As String, tmpZ As String, tmptunit As String, DaRow1_s_adj As Long    '24/1/2005
Dim tmpDAgeU As String    '8/3/2005
On Error GoTo E
cur = ColName(idxM1_s(idex))  '31/3/2005 move to top
If NHead_s = 1 Then  '24/1/2005 add *_adj
   DaRow1_s_adj = DaRow1_s + 1
   Range(cur & DaRow1_s).value = "Cent_" & mTitle(idex)   '4/3/2005
Else
   DaRow1_s_adj = DaRow1_s
End If
If DaRow1_s_adj > DaRow2_s Then Exit Sub
j1 = idxSex_s - 1 - idxM1_s(idex)   '7/1/2005 M2->M1 for calc centiles in frmSDSfx
If Datetype_s = 0 Then j2 = idxAge_s - idxM1_s(idex) Else j2 = idxAgeD_s - idxM1_s(idex)  '2/2/2005
j3 = idxM2_s(idex) - idxM1_s(idex)  'remove 6/12/2004, 7/1/2005 revocer
'cur = ColName(idxM1_s(idex))   'use 256 columns, 31/3/2005 move to top
Range(cur & DaRow1_s_adj).Select
tmpName = Chr(34) & mName(idex) & Chr(34)    '17/11/2004
tmpDfile = Chr(34) & DataFile & Chr(34)      '23/11/2004
tmpaName = Chr(34) & tName & Chr(34)         '29/11/2004
'tmptunit = Chr(34) & tUnit & Chr(34)       '3/12/2004, remove 8/3/2005
tmpDAgeU = Chr(34) & frmSDSFx!lblAgeU.Caption & Chr(34)       '8/3/2005
Dim Ssex As Variant  '4/3/2005
Select Case iSex     '4/3/2005
   Case 0
        Ssex = Chr(34) & "M" & Chr(34)
   Case 1
        Ssex = Chr(34) & "F" & Chr(34)
   Case Is > 1
        Ssex = "RC[" & j1 & "]"
End Select
Select Case idxGest_s   '24/1/2005
    Case 0  'not use gestation
          ActiveCell.FormulaR1C1 = "=cCentile(" & Ssex & ",RC[" & j2 & "]," & tmpDAgeU & ",RC[" & j3 & "]," & tmpaName & ", " & tmpName & ", " & tmpDfile & ")"   '7/1/2005 recover
    Case Is > 0
         j4 = idxGest_s - idxM1_s(idex)
         ActiveCell.FormulaR1C1 = "=cCentileg(" & Ssex & ",RC[" & j4 & "],RC[" & j2 & "]," & tmpDAgeU & ",RC[" & j3 & "]," & tmpaName & ", " & tmpName & ", " & tmpDfile & ")"   '24/1/2005
End Select
If DaRow2_s > DaRow1_s_adj Then
   Range(cur & DaRow1_s_adj).Select
   'Selection.NumberFormat = "0.000"  '31/3/2005 for decimals, remove 29/11/2005
   Selection.AutoFill Destination:=Range(cur & DaRow1_s_adj & ":" & cur & DaRow2_s), Type:=xlFillDefault
End If

Exit Sub

E:
'MsgBox "Error in CentYMWD", 48, "LMSgrowth"  'remove 10/9/2004
End Sub






Function cFNCg(Fidx As Integer, sexRange As Variant, gRange As Variant, tRange As Variant, DAgeU As String, Yrange As Variant, agname As String, meaName As String, Dfile As String, Optional Crange1 As Variant, Optional Crange2 As Variant) As Variant
'cSDS + gestation
Dim LL As Single, MM As Single, SS As Single, tmin As Single, tmax As Single
Dim cols As Integer, t As Single, Y As Single, AgeCol As String, MeaCol As String, gt As Single
Dim k As Long, ScrFail As Integer, DataAgeCol As String, DataMeaCol As String
Dim AgeR As Single, RAgeU As String, Nm As Integer   '7/3/2005

'On Error Resume Next
On Error GoTo E
cFNCg = unknown    '15/9/2004 movr from bottom

AgeCol = agname       '29/11/2004
MeaCol = meaName      '17/11/2004

If IsBookOpen(Dfile) = False Then
   If Not IsDiskFile(Dfile) Then
      Exit Function
   Else
      Workbooks.Open Dfile
   End If
End If
If IsNameExist(AgeCol, Dfile) = False Then
   Exit Function
End If
If IsNameExist(MeaCol, Dfile) = False Then
   Exit Function
End If
DataAgeCol = Dfile & "!" & AgeCol
DataMeaCol = Dfile & "!" & MeaCol

'check sex
If IsMissing(sexRange) = True Then GoTo E
If sexRange = "" Then GoTo E
If (Not IsNumeric(sexRange)) Then
    If UCase(Trim(sexRange)) = "M" Or UCase(Trim(sexRange)) = "MALE" Then   '17/8/2005
       cols = 3
    Else
      If UCase(Trim(sexRange)) = "F" Or UCase(Trim(sexRange)) = "FEMALE" Then   '17/8/2005
         cols = 6
      Else
         GoTo E
      End If
    End If
Else
    If sexRange = 1 Then
       cols = 3
    Else
       If sexRange = 2 Then
          cols = 6
       Else
          GoTo E
       End If
    End If
End If

'Check age
If IsMissing(tRange) = True Then GoTo E
If tRange = "" Then GoTo E
If (Not IsNumeric(tRange)) Then GoTo E
If IsMissing(gRange) = True Then GoTo E     '3/12/2004  for gestation
If gRange = "" Then GoTo E                  '3/12/2004  for gestation
If (Not IsNumeric(gRange)) Then GoTo E      '3/12/2004  for gestation
k = Range(DataAgeCol).Rows.Count
tmin = Range(DataAgeCol).Rows(1)
tmax = Range(DataAgeCol).Rows(k)
gt = gRange
'nm = InStrRev(AgeCol, "_")     '7/3/2005
Nm = RevSearch(AgeCol, "_")    '22/3/2005
If Nm <> 0 Then RAgeU = Mid(AgeCol, Nm + 1, Len(AgeCol) - Nm) Else GoTo E '7/3/2005
getAgeRate DAgeU, RAgeU, AgeR   '7/3/2005
t = tRange * AgeR  '3/2/2005
'Select Case agUnit    'gRang in wk
Select Case RAgeU    '7/3/2005 gestation in wk
     Case "yr", "year", "years"
           t = t - (40 - gt) * 7 / 365.25
     Case "mo", "month", "months"
           t = t - (40 - gt) * 84 / 365.25
     Case "wk", "week", "weeks"
           t = t - (40 - gt)
     Case "dy", "day", "days"
           t = t - (40 - gt) * 7
     Case Else
          GoTo E
End Select
' tmin= -0.326 and tmax = 23 in lmsdata.xls
If (t < tmin) Or (t > tmax) Then GoTo E

'check yy, ----03/05/2011 move to after check Fidx
'If IsMissing(Yrange) Then GoTo E
'If Yrange = "" Then GoTo E
'If (Not IsNumeric(Yrange)) Then GoTo E
'------------------move to after check covariate 03/05/2011
    
'check covariate of lung function 3/4/2007,15/5/2007,22/5/2007,21/6/2007----
If IsMissing(Fidx) Then GoTo E
Dim Rt As Long, Cl As Integer, err As Integer, cov1 As Single, cov2 As Single
Rt = Range(DataAgeCol).Row
Cl = Range(DataMeaCol).Column + cols - 3
Select Case Rt   'need for refresh existing results
   Case 10
       CovChk Dfile, Rt - 3, Cl, Crange1, cov1, err
       If err = 1 Then GoTo E
   Case 12
       CovChk Dfile, Rt - 4, Cl, Crange1, cov1, err
       If err = 1 Then GoTo E
       CovChk Dfile, Rt - 3, Cl, Crange2, cov2, err
       If err = 1 Then GoTo E
End Select
'-------

'check yy
If IsMissing(Yrange) And Fidx < 4 Then GoTo E     'add Fidx < 4 on 03/05/2011
If Yrange = "" And Fidx < 4 Then GoTo E               'add Fidx < 4 on 03/05/2011
If (Not IsNumeric(Yrange)) And Fidx < 4 Then GoTo E       'add Fidx < 4 on 03/05/2011
Y = Yrange
If Y <= 0 And Fidx < 4 Then GoTo E   'add Fidx < 4 on 03/05/2011
BinarySearch t, DataAgeCol, DataMeaCol, cols, LL, MM, SS, ScrFail
If ScrFail = 1 Then GoTo E

'add for covariate of lung function 3/4/2007, 11/6/2007----
CovAdd Dfile, Rt, Cl, t, cov1, cov2, LL
CovAdd Dfile, Rt, Cl + 1, t, cov1, cov2, MM
CovAdd Dfile, Rt, Cl + 2, t, cov1, cov2, SS
'-----
'add for Lung finction 6 types of output 21/6/2007 ----
Select Case Fidx
   Case 1  'SDS
        cFNCg = zLMS(Y, LL, MM, SS)   '21/6/2007 move codes to zLMS
   Case 2  'centiles
        cFNCg = PZ(zLMS(Y, LL, MM, SS)) * 100
   Case 3  '%Predicted
        cFNCg = 100 * Y / MM
   Case 4  'Predicted
        cFNCg = MM
   Case 5  '%CV
        cFNCg = SS * 100
   Case 6  'Skewness
        cFNCg = LL
    Case 7  'lower limit normal - LLN based on 5th centile 18/3/2011
        cFNCg = LLN(LL, MM, SS)
End Select
'------------------------
'If Abs(cFNCg) >= Zcutoff Then GoTo E  'remove 22/6/2007
'cFNCg = Format(cFNCg, "#0.00")   'eg 12.295 -> 12.30  13/5/2003
'cFNCg = Round(cFNCg, 3)          'eg 12.295 -> 12.3  22/5/2003 not available in Mac
'-------------------------remove 9/11/2007
'Dim Ntmp As Integer
'Ntmp = 10 ^ idxDec_P  '29/11/2005 user determined, default 2
'cFNCg = Int(cFNCg * Ntmp + 0.5) / Ntmp
'-------------------------remove 9/11/2007
Exit Function

E:
'MsgBox "problem in cFNCg", 48, "LMSgrowth"   'remove 15/9/2004

End Function
Function cSDSg(sexRange As Variant, gRange As Variant, tRange As Variant, DAgeU As String, Yrange As Variant, agname As String, meaName As String, Dfile As String) As Variant
'cSDS + gestation
Dim LL As Single, MM As Single, SS As Single, tmin As Single, tmax As Single
Dim cols As Integer, t As Single, Y As Single, AgeCol As String, MeaCol As String, gt As Single
Dim k As Long, ScrFail As Integer, DataAgeCol As String, DataMeaCol As String
Dim AgeR As Single, RAgeU As String, Nm As Integer   '7/3/2005

'On Error Resume Next
On Error GoTo E
cSDSg = unknown

AgeCol = agname       '29/11/2004
MeaCol = meaName      '17/11/2004

If IsBookOpen(Dfile) = False Then
   If Not IsDiskFile(Dfile) Then
      Exit Function
   Else
      Workbooks.Open Dfile
   End If
End If
If IsNameExist(AgeCol, Dfile) = False Then
   Exit Function
End If
If IsNameExist(MeaCol, Dfile) = False Then
   Exit Function
End If
DataAgeCol = Dfile & "!" & AgeCol
DataMeaCol = Dfile & "!" & MeaCol

'check sex
    If IsMissing(sexRange) = True Then GoTo E
    If sexRange = "" Then GoTo E
    If (Not IsNumeric(sexRange)) Then
        If UCase(Trim(sexRange)) = "M" Or UCase(Trim(sexRange)) = "MALE" Then   '17/8/2005
           cols = 3
        Else
          If UCase(Trim(sexRange)) = "F" Or UCase(Trim(sexRange)) = "FEMALE" Then   '17/8/2005
             cols = 6
          Else
             GoTo E
          End If
        End If
    Else
       If sexRange = 1 Then
          cols = 3
       Else
          If sexRange = 2 Then
             cols = 6
          Else
             GoTo E
          End If
       End If
    End If
    'Check age
    If IsMissing(tRange) = True Then GoTo E
    If tRange = "" Then GoTo E
    If (Not IsNumeric(tRange)) Then GoTo E
    If IsMissing(gRange) = True Then GoTo E     '3/12/2004  for gestation
    If gRange = "" Then GoTo E                  '3/12/2004  for gestation
    If (Not IsNumeric(gRange)) Then GoTo E      '3/12/2004  for gestation
    k = Range(DataAgeCol).Rows.Count
    tmin = Range(DataAgeCol).Rows(1)
    tmax = Range(DataAgeCol).Rows(k)
    gt = gRange
    'nm = InStrRev(AgeCol, "_")     '7/3/2005
    Nm = RevSearch(AgeCol, "_")    '22/3/2005
    If Nm <> 0 Then RAgeU = Mid(AgeCol, Nm + 1, Len(AgeCol) - Nm) Else GoTo E '7/3/2005
    getAgeRate DAgeU, RAgeU, AgeR   '7/3/2005
    t = tRange * AgeR  '3/2/2005
    'Select Case agUnit    'gRang in wk
    Select Case RAgeU    '7/3/2005 gestation in wk
         Case "yr", "year", "years"
               t = t - (40 - gt) * 7 / 365.25
         Case "mo", "month", "months"
               t = t - (40 - gt) * 84 / 365.25
         Case "wk", "week", "weeks"
               t = t - (40 - gt)
         Case "dy", "day", "days"
               t = t - (40 - gt) * 7
         Case Else
              GoTo E
   End Select
    ' tmin= -0.326 and tmax = 23 in lmsdata.xls
    If (t < tmin) Or (t > tmax) Then GoTo E
   'check yy
    If IsMissing(Yrange) Then GoTo E
    If Yrange = "" Then GoTo E
    If (Not IsNumeric(Yrange)) Then GoTo E

Y = Yrange
If Y <= 0 Then GoTo E
BinarySearch t, DataAgeCol, DataMeaCol, cols, LL, MM, SS, ScrFail
If ScrFail = 1 Then GoTo E
cSDSg = zLMS(Y, LL, MM, SS)   '21/6/2007 use zLMS for calc z

'cSDSg = Format(cSDSg, "#0.00")   'eg 12.295 -> 12.30  13/5/2003
'If Abs(cSDSg) >= Zcutoff Then GoTo E  'remove 6/3/2009
'cSDSg = Round(cSDSg, 3)           'eg 12.295 -> 12.3  22/5/2003 not available in Mac
'cSDSg = Int(cSDSg * 100 + 0.5) / 100    '10/6/2003, remove 29/11/2005
'-------------------------remove 9/11/2007
'Dim Ntmp As Integer
'Ntmp = 10 ^ idxDec_P
'cSDSg = Int(cSDSg * Ntmp + 0.5) / Ntmp   '29/11/2005
'-------------------------remove 9/11/2007
Exit Function

E:
'MsgBox "problem in cSDSg", 48, "LMSgrowth"   'remove 15/9/2004

End Function
Function cSDg(Fidx As Integer, sexRange As Variant, gRange As Variant, tRange As Variant, DAgeU As String, Yrange As Variant, agname As String, meaName As String, Dfile As String) As Variant
'24/7/2007 copy cSDSg for six outcomes adding Sidx
Dim LL As Single, MM As Single, SS As Single, tmin As Single, tmax As Single
Dim cols As Integer, t As Single, Y As Single, AgeCol As String, MeaCol As String, gt As Single
Dim k As Long, ScrFail As Integer, DataAgeCol As String, DataMeaCol As String
Dim AgeR As Single, RAgeU As String, Nm As Integer   '7/3/2005

'On Error Resume Next
On Error GoTo E
cSDg = unknown

AgeCol = agname       '29/11/2004
MeaCol = meaName      '17/11/2004

If IsBookOpen(Dfile) = False Then
   If Not IsDiskFile(Dfile) Then
      Exit Function
   Else
      Workbooks.Open Dfile
   End If
End If
If IsNameExist(AgeCol, Dfile) = False Then
   Exit Function
End If
If IsNameExist(MeaCol, Dfile) = False Then
   Exit Function
End If
DataAgeCol = Dfile & "!" & AgeCol
DataMeaCol = Dfile & "!" & MeaCol

'check sex
If IsMissing(sexRange) = True Then GoTo E
If sexRange = "" Then GoTo E
If (Not IsNumeric(sexRange)) Then
    If UCase(Trim(sexRange)) = "M" Or UCase(Trim(sexRange)) = "MALE" Then   '17/8/2005
       cols = 3
    Else
      If UCase(Trim(sexRange)) = "F" Or UCase(Trim(sexRange)) = "FEMALE" Then   '17/8/2005
         cols = 6
      Else
         GoTo E
      End If
    End If
Else
    If sexRange = 1 Then
       cols = 3
    Else
       If sexRange = 2 Then
          cols = 6
       Else
          GoTo E
       End If
    End If
End If

'Check age
If IsMissing(tRange) = True Then GoTo E
If tRange = "" Then GoTo E
If (Not IsNumeric(tRange)) Then GoTo E
If IsMissing(gRange) = True Then GoTo E     '3/12/2004  for gestation
If gRange = "" Then GoTo E                  '3/12/2004  for gestation
If (Not IsNumeric(gRange)) Then GoTo E      '3/12/2004  for gestation
k = Range(DataAgeCol).Rows.Count
tmin = Range(DataAgeCol).Rows(1)
tmax = Range(DataAgeCol).Rows(k)
gt = gRange
'nm = InStrRev(AgeCol, "_")     '7/3/2005
Nm = RevSearch(AgeCol, "_")    '22/3/2005
If Nm <> 0 Then RAgeU = Mid(AgeCol, Nm + 1, Len(AgeCol) - Nm) Else GoTo E '7/3/2005
getAgeRate DAgeU, RAgeU, AgeR   '7/3/2005
t = tRange * AgeR  '3/2/2005
'Select Case agUnit    'gRang in wk
Select Case RAgeU    '7/3/2005 gestation in wk
     Case "yr", "year", "years"
          t = t - (40 - gt) * 7 / 365.25
     Case "mo", "month", "months"
          t = t - (40 - gt) * 84 / 365.25
     Case "wk", "week", "weeks"
          t = t - (40 - gt)
     Case "dy", "day", "days"
          t = t - (40 - gt) * 7
     Case Else
          GoTo E
End Select
' tmin= -0.326 and tmax = 23 in lmsdata.xls
If (t < tmin) Or (t > tmax) Then GoTo E
   
'check yy
If IsMissing(Yrange) And Fidx < 4 Then GoTo E    'add Fidx < 4 03/05/2011
If Yrange = "" And Fidx < 4 Then GoTo E                      'add Fidx < 4 03/05/2011
If (Not IsNumeric(Yrange)) And Fidx < 4 Then GoTo E          'add Fidx < 4 03/05/2011
'If IsMissing(Yrange) Then GoTo E
'If Yrange = "" Then GoTo E
'If (Not IsNumeric(Yrange)) Then GoTo E
Y = Yrange
If Y <= 0 And Fidx < 4 Then GoTo E       'add Fidx < 4 03/05/2011
'If Y <= 0 Then GoTo E
BinarySearch t, DataAgeCol, DataMeaCol, cols, LL, MM, SS, ScrFail
If ScrFail = 1 Then GoTo E
'cSDg = zLMS(Y, LL, MM, SS)   '21/6/2007 use zLMS for calc z
Select Case Fidx   '24/7/2007 add copy from cSD
   Case 1  'SDS
        cSDg = zLMS(Y, LL, MM, SS)
   Case 2  'centiles
        cSDg = PZ(zLMS(Y, LL, MM, SS)) * 100
   Case 3  '%Predicted
        cSDg = 100 * Y / MM
   Case 4  'Predicted
        cSDg = MM
   Case 5  '%CV
        cSDg = SS * 100
   Case 6  'Skewness
        cSDg = LL
   Case 7  'lower limit notnal base on 5th centile - LLN
        cSDg = LLN(LL, MM, SS)
End Select
'cSDg = Format(cSDg, "#0.00")   'eg 12.295 -> 12.30  13/5/2003
'If Abs(cSDg) >= Zcutoff Then GoTo E
'cSDg = Round(cSDg, 3)           'eg 12.295 -> 12.3  22/5/2003 not available in Mac
'cSDg = Int(cSDg * 100 + 0.5) / 100    '10/6/2003, remove 29/11/2005
'-------------------------remove 9/11/2007
'Dim Ntmp As Integer
'Ntmp = 10 ^ idxDec_P
'cSDg = Int(cSDg * Ntmp + 0.5) / Ntmp   '29/11/2005
'-------------------------remove 9/11/2007
Exit Function

E:
'MsgBox "problem in cSDg", 48, "LMSgrowth"   'remove 15/9/2004

End Function
Sub getHelp(HelpID As Long)
'1/4/2011

If CPU = "Mac" Then
   MsgBox (MacHelp1 & Chr(13) & MacHelp2 & Chr(13) & MacHelp3), 48, "LMSgrowth"    '3/5/2007
Else
   'Call HtmlHelp(0, Workbooks("growth.xls").Path & PS & "growth.chm", HH_HELP_CONTEXT, HelpID)   '2 for Introduction topic
   Call HtmlHelp(0, AddIns("growth").Path & PS & "growth.chm", HH_HELP_CONTEXT, HelpID)
End If

'---------------------------remove *.hlp codes 1/4/2011
'If CPU = "Mac" Then
'   MsgBox (MacHelp1 & Chr(13) & MacHelp2 & Chr(13) & MacHelp3), 48, "LMSgrowth"    '3/5/2007
'Else
'   Application.Help Workbooks("growth.xls").Path & PS & "growth.chm", HelpID     'if use WinHelp
'   'Application.Help AddIns("growth").Path & PS & "growth.hlp", HelpID
'End If
'---------------------------remove *.hlp codes

End Sub

Sub getNameLLN()
'25/3/2011, 6/4/2011 add ppLLN for cobLLN display

pLLN(1) = "0.4": zLLN(1) = -2.66934
pLLN(2) = "1": zLLN(2) = -2.32635
pLLN(3) = "2": zLLN(3) = -1.99908
pLLN(4) = "2.5": zLLN(4) = -1.95996
pLLN(5) = "3": zLLN(5) = -1.88079
pLLN(6) = "5": zLLN(6) = -1.64485
ppLLN(1) = "0.4* (z = -2.67)"
ppLLN(2) = "1"
ppLLN(3) = "2* (z = -2)"
ppLLN(4) = "2.5"
ppLLN(5) = "3"
ppLLN(6) = "5"

End Sub

Function LLN(LL As Single, MM As Single, SS As Single) As Variant
'18/3/2011 for lower limit normal based on 5th centile
'codes copied from cCent
Dim LSY As Single, zY As Single

'zY = -1.64485   'for 5th centile for Philip to use v2.72
zY = zLLN(idxLLN)      '25/3/2011

LLN = unknown2
If LL = 1 Then
   LLN = 1 + SS * zY
Else
   If LL <> 0 Then
      LSY = LL * SS * zY     '27/5/2009
      If LSY > -1 Then     '27/5/2009
            LLN = (1 + LSY) ^ (1 / LL)
      Else
            GoTo E
      End If
   Else
      LLN = Exp(SS * zY)
   End If
End If
LLN = LLN * MM

E:
End Function

Sub OpenPreference()
'25/3/2011

Application.ScreenUpdating = False
On Error GoTo E
CPU = Application.OperatingSystem
PS = Application.PathSeparator
If CPU = "Mac" Then ZoomSize = ZoomMac Else ZoomSize = ZoomPC
getNameLLN    '25/3/2011 called in Makemenu, here is only for my work test
frmPreference.Show

Application.ScreenUpdating = True
Exit Sub

E:
Application.ScreenUpdating = True
End Sub

Sub SetColFormat(cur As String)
 '9/11/2007
Columns(cur).Select
Selection.NumberFormat = "0.00"
End Sub

Function showP(pp As Variant) As String
'22/6/2007

If pp <= 99 And pp >= 1 Then
   showP = Format(Int(pp + 0.5), "##0")
Else
   If pp < 1 Then
      pp = Int(pp * 10 + 0.5) / 10
      If pp < 0.1 Then
         showP = "< 0.1"
      Else
         showP = Format(pp, "##0.0")
      End If
   Else
      pp = Int(pp * 10 + 0.5) / 10
      If pp > 99.9 Then
         showP = "> 99.9"
      Else
         showP = Format(pp, "##0.0")
      End If
   End If
End If

End Function


Sub getClearCol()
'21/9/2004 clear measurement cols only if change to a new ref for SDSfx and centilefx
'18/6/2007 clear all
getClearColS   'SDS & Centile
getClearColC   'SDS with covariate
getClearColI   'IOTF
getClearColG   'Onechild

'18/6/2007 remove --------------------------------------
'Dim i As Integer
''frmSDS*
'For i = 1 To MaxN   '6
'    idxM1_s(i) = 0: idxM2_s(i) = 0: idxM3_s(i) = 0
'Next i
'If NumCov > 0 Then '18'6'2007
'      idxCov1_s = 0: idxCov2_s = 0
'End If
''idxSex_s = 0: idxSex_I = 0: idxSex_g = 0
''idxAge_s = 0: idxAge_I = 0: idxAge1_g = 0: idxAge2_g = 0
''idxSc1_g = 0: idxSc2_g = 0: idxSc1_g_o = 0: idxSc2_g_o = 0
''idxWT1_g = 0: idxWT2_g = 0: idxSDS_g = 0
''DaRow1_s = 0: DaRow2_s = 0: DaRow1_I = 0: DaRow2_I = 0: DatRow1_g = 0: DatRow2_g = 0:
''idxM1_I = 0: idxM2_I = 0
'18/6/2007 remove --------------------------------------

End Sub






Sub CovChk(Dfile As String, r As Long, c As Integer, Crange As Variant, cov As Single, err As Integer)
On Error GoTo E
Dim s As String
err = 0
s = Mid(Dfile, 1, Len(Dfile) - 4)
If Workbooks(Dfile).Sheets(s).Cells(r, c) <> 0 Or Workbooks(Dfile).Sheets(s).Cells(r, c + 1) <> 0 Or Workbooks(Dfile).Sheets(s).Cells(r, c + 2) <> 0 Then    'if coef of cov1<>0
   If IsMissing(Crange) = True Then GoTo E
   If Crange = "" Then GoTo E
   If (Not IsNumeric(Crange)) Then
      GoTo E
   Else
      If Crange <= 0 Then
         GoTo E
      Else
         cov = Crange
      End If
  End If
End If
Exit Sub
E:
err = 1
End Sub

Sub getClearColG()
'18/6/2007 copy from cmdReset of frmWtGain
idxSex_g = 0: idxAge1_g = 0: idxAge2_g = 0: idxSDS_g = 0
idxSc1_g = 2: idxSc2_g = 2   'week as default
idxWT1_g = 0: idxWT2_g = 0
NHead_g = 0: DatRow1_g = 0: DatRow2_g = 0
End Sub

Sub getClearColI()
'18/6/2007 copy from cmdReset of frmIOTFCo
idxSex_I = 0: idxAge_I = 0
IaUnit = 0: NHead_I = 0
DaRow1_I = 0: DaRow2_I = 0
idxM1_I = 0: idxM2_I = 0
idxWt_I = 0: idxHt_I = 0: idxWH_I = 0: NuseWH_I = 0    '15/8/2005
End Sub

Sub getClearColS()
'18/6/2007 copy from cmdReSet of frmSDSFx
Dim i As Integer
idxSex_s = 0: idxGest_s = 0: idxBirth_s = 0: idxMeaDate_s = 0
idxAge_s = 0: idxAgeD_s = 0: SaUnit = 0: idxStoM_s = 0
For i = 1 To MaxN
    idxM1_s(i) = 0: idxM2_s(i) = 0
Next i
DaRow1_s = 0: DaRow2_s = 0
Datetype_s = 0: NHead_s = 0

End Sub

Sub getClearColC()
'20/6/2007 copy from cmdReSet of frmSDSCov
Dim i As Integer
idxSex_c = 0: idxGest_c = 0: idxBirth_c = 0: idxMeaDate_c = 0
idxAge_c = 0: idxAgeD_c = 0: CaUnit = 0: idxStoM_c = 0
For i = 1 To MaxN
    idxM1_c(i) = 0: idxM2_c(i) = 0
Next i
DaRow1_c = 0: DaRow2_c = 0
Datetype_c = 0: NHead_c = 0
idxCov1_c = 0: idxCov2_c = 0
Fidx_c = 1   '22/6/2007
End Sub





Sub getDefXYused()
'25/11/2004 forc the sequence of names in British1990.xls as default
ReDim mName(MaxN), mTitle(MaxN), mUnit(MaxN)

tName = "x_Age_yr": tTitle = "Age": tUnit = "year"

mName(1) = "y_Height_cm": mName(2) = "y_Weight_kg": mName(4) = "y_Head_cm"   '23/3/2005
mName(3) = "y_BMI_kglm2": mName(5) = "y_Sitht_cm": mName(6) = "y_Legln_cm"   '8/8/2007 kgm2->kglm2
mTitle(1) = "Height": mTitle(2) = "Weight": mTitle(3) = "BMI"
mTitle(4) = "Head": mTitle(5) = "Sitht": mTitle(6) = "Legln"
mUnit(1) = "cm": mUnit(2) = "kg": mUnit(3) = "kglm2"    '8/8/2007 kg/m2->kglm2
mUnit(4) = "cm": mUnit(5) = "cm": mUnit(6) = "cm"
NameUsed = MaxN

WTat = 2: OkAge = 1: OkWT = 1: OkHWB = 1
SaUnit = 1: IaUnit = 1: IaUnit_o = 1: CaUnit = 1
idxSc1_g = 0: idxSc2_g = 0: idxSc1_g_o = 0: idxSc2_g_o = 0   'year
OKHSL = 3
NumCov = 0
End Sub


Sub getFNClist()
'21/6/2007, 18/3/2011 add LLN (lower limited normal) 6->7
ReDim FNClist(7)

FNClist(1) = "SDS"
FNClist(2) = "Centile"
FNClist(3) = "%Predicted"
FNClist(4) = "Predicted"
FNClist(5) = "%CV"
FNClist(6) = "Skewness"
If idxLLN = 0 Then idxLLN = 6
FNClist(7) = "LLN " & pLLN(idxLLN)
FNClist(7) = FNClist(7)
End Sub

Sub getIOTFf()
'20/04/2007 for 30,25,18.5,17,16 by sex
'0-t,1-16,2-17,3-18.5,4-25,5-30, IOTFm-male IOTFf-female
IOTFf(1, 0) = 2: IOTFf(1, 1) = 13.24: IOTFf(1, 2) = 13.9: IOTFf(1, 3) = 14.83: IOTFf(1, 4) = 18.02: IOTFf(1, 5) = 19.81
IOTFf(2, 0) = 2.5: IOTFf(2, 1) = 13.1: IOTFf(2, 2) = 13.74: IOTFf(2, 3) = 14.63: IOTFf(2, 4) = 17.76: IOTFf(2, 5) = 19.55
IOTFf(3, 0) = 3: IOTFf(3, 1) = 12.98: IOTFf(3, 2) = 13.6: IOTFf(3, 3) = 14.47: IOTFf(3, 4) = 17.56: IOTFf(3, 5) = 19.36
IOTFf(4, 0) = 3.5: IOTFf(4, 1) = 12.86: IOTFf(4, 2) = 13.47: IOTFf(4, 3) = 14.32: IOTFf(4, 4) = 17.4: IOTFf(4, 5) = 19.23
IOTFf(5, 0) = 4: IOTFf(5, 1) = 12.73: IOTFf(5, 2) = 13.34: IOTFf(5, 3) = 14.19: IOTFf(5, 4) = 17.28: IOTFf(5, 5) = 19.15
IOTFf(6, 0) = 4.5: IOTFf(6, 1) = 12.61: IOTFf(6, 2) = 13.21: IOTFf(6, 3) = 14.06: IOTFf(6, 4) = 17.19: IOTFf(6, 5) = 19.12
IOTFf(7, 0) = 5: IOTFf(7, 1) = 12.5: IOTFf(7, 2) = 13.09: IOTFf(7, 3) = 13.94: IOTFf(7, 4) = 17.15: IOTFf(7, 5) = 19.17
IOTFf(8, 0) = 5.5: IOTFf(8, 1) = 12.4: IOTFf(8, 2) = 12.99: IOTFf(8, 3) = 13.86: IOTFf(8, 4) = 17.2: IOTFf(8, 5) = 19.34
IOTFf(9, 0) = 6: IOTFf(9, 1) = 12.32: IOTFf(9, 2) = 12.93: IOTFf(9, 3) = 13.82: IOTFf(9, 4) = 17.34: IOTFf(9, 5) = 19.65
IOTFf(10, 0) = 6.5: IOTFf(10, 1) = 12.28: IOTFf(10, 2) = 12.9: IOTFf(10, 3) = 13.82: IOTFf(10, 4) = 17.53: IOTFf(10, 5) = 20.08
IOTFf(11, 0) = 7: IOTFf(11, 1) = 12.26: IOTFf(11, 2) = 12.91: IOTFf(11, 3) = 13.86: IOTFf(11, 4) = 17.75: IOTFf(11, 5) = 20.51
IOTFf(12, 0) = 7.5: IOTFf(12, 1) = 12.27: IOTFf(12, 2) = 12.95: IOTFf(12, 3) = 13.93: IOTFf(12, 4) = 18.03: IOTFf(12, 5) = 21.01
IOTFf(13, 0) = 8: IOTFf(13, 1) = 12.31: IOTFf(13, 2) = 13: IOTFf(13, 3) = 14.02: IOTFf(13, 4) = 18.35: IOTFf(13, 5) = 21.57
IOTFf(14, 0) = 8.5: IOTFf(14, 1) = 12.37: IOTFf(14, 2) = 13.08: IOTFf(14, 3) = 14.14: IOTFf(14, 4) = 18.69: IOTFf(14, 5) = 22.18
IOTFf(15, 0) = 9: IOTFf(15, 1) = 12.44: IOTFf(15, 2) = 13.18: IOTFf(15, 3) = 14.28: IOTFf(15, 4) = 19.07: IOTFf(15, 5) = 22.81
IOTFf(16, 0) = 9.5: IOTFf(16, 1) = 12.53: IOTFf(16, 2) = 13.29: IOTFf(16, 3) = 14.43: IOTFf(16, 4) = 19.45: IOTFf(16, 5) = 23.46
IOTFf(17, 0) = 10: IOTFf(17, 1) = 12.64: IOTFf(17, 2) = 13.43: IOTFf(17, 3) = 14.61: IOTFf(17, 4) = 19.86: IOTFf(17, 5) = 24.11
IOTFf(18, 0) = 10.5: IOTFf(18, 1) = 12.78: IOTFf(18, 2) = 13.59: IOTFf(18, 3) = 14.81: IOTFf(18, 4) = 20.29: IOTFf(18, 5) = 24.77
IOTFf(19, 0) = 11: IOTFf(19, 1) = 12.95: IOTFf(19, 2) = 13.79: IOTFf(19, 3) = 15.05: IOTFf(19, 4) = 20.74: IOTFf(19, 5) = 25.42
IOTFf(20, 0) = 11.5: IOTFf(20, 1) = 13.15: IOTFf(20, 2) = 14.01: IOTFf(20, 3) = 15.32: IOTFf(20, 4) = 21.2: IOTFf(20, 5) = 26.05
IOTFf(21, 0) = 12: IOTFf(21, 1) = 13.39: IOTFf(21, 2) = 14.28: IOTFf(21, 3) = 15.62: IOTFf(21, 4) = 21.68: IOTFf(21, 5) = 26.67
IOTFf(22, 0) = 12.5: IOTFf(22, 1) = 13.65: IOTFf(22, 2) = 14.56: IOTFf(22, 3) = 15.93: IOTFf(22, 4) = 22.14: IOTFf(22, 5) = 27.24
IOTFf(23, 0) = 13: IOTFf(23, 1) = 13.92: IOTFf(23, 2) = 14.85: IOTFf(23, 3) = 16.26: IOTFf(23, 4) = 22.58: IOTFf(23, 5) = 27.76
IOTFf(24, 0) = 13.5: IOTFf(24, 1) = 14.2: IOTFf(24, 2) = 15.14: IOTFf(24, 3) = 16.57: IOTFf(24, 4) = 22.98: IOTFf(24, 5) = 28.2
IOTFf(25, 0) = 14: IOTFf(25, 1) = 14.48: IOTFf(25, 2) = 15.43: IOTFf(25, 3) = 16.88: IOTFf(25, 4) = 23.34: IOTFf(25, 5) = 28.57
IOTFf(26, 0) = 14.5: IOTFf(26, 1) = 14.75: IOTFf(26, 2) = 15.72: IOTFf(26, 3) = 17.18: IOTFf(26, 4) = 23.66: IOTFf(26, 5) = 28.87
IOTFf(27, 0) = 15: IOTFf(27, 1) = 15.01: IOTFf(27, 2) = 15.98: IOTFf(27, 3) = 17.45: IOTFf(27, 4) = 23.94: IOTFf(27, 5) = 29.11
IOTFf(28, 0) = 15.5: IOTFf(28, 1) = 15.25: IOTFf(28, 2) = 16.22: IOTFf(28, 3) = 17.69: IOTFf(28, 4) = 24.17: IOTFf(28, 5) = 29.29
IOTFf(29, 0) = 16: IOTFf(29, 1) = 15.46: IOTFf(29, 2) = 16.44: IOTFf(29, 3) = 17.91: IOTFf(29, 4) = 24.37: IOTFf(29, 5) = 29.43
IOTFf(30, 0) = 16.5: IOTFf(30, 1) = 15.63: IOTFf(30, 2) = 16.62: IOTFf(30, 3) = 18.09: IOTFf(30, 4) = 24.54: IOTFf(30, 5) = 29.56
IOTFf(31, 0) = 17: IOTFf(31, 1) = 15.78: IOTFf(31, 2) = 16.77: IOTFf(31, 3) = 18.25: IOTFf(31, 4) = 24.7: IOTFf(31, 5) = 29.69
IOTFf(32, 0) = 17.5: IOTFf(32, 1) = 15.9: IOTFf(32, 2) = 16.89: IOTFf(32, 3) = 18.38: IOTFf(32, 4) = 24.85: IOTFf(32, 5) = 29.84
IOTFf(33, 0) = 18: IOTFf(33, 1) = 16: IOTFf(33, 2) = 17: IOTFf(33, 3) = 18.5: IOTFf(33, 4) = 25: IOTFf(33, 5) = 30
End Sub

Sub getIOTFm()
'20/04/2007 for 30,25,18.5,17,16 by sex
'0-t,1-16,2-17,3-18.5,4-25,5-30, IOTFm-male IOTFf-female
IOTFm(1, 0) = 2: IOTFm(1, 4) = 18.41: IOTFm(1, 5) = 20.09: IOTFm(1, 3) = 15.14: IOTFm(1, 2) = 14.12: IOTFm(1, 1) = 13.37
IOTFm(2, 0) = 2.5: IOTFm(2, 4) = 18.13: IOTFm(2, 5) = 19.8: IOTFm(2, 3) = 14.92: IOTFm(2, 2) = 13.94: IOTFm(2, 1) = 13.22
IOTFm(3, 0) = 3: IOTFm(3, 4) = 17.89: IOTFm(3, 5) = 19.57: IOTFm(3, 3) = 14.74: IOTFm(3, 2) = 13.79: IOTFm(3, 1) = 13.09
IOTFm(4, 0) = 3.5: IOTFm(4, 4) = 17.69: IOTFm(4, 5) = 19.39: IOTFm(4, 3) = 14.57: IOTFm(4, 2) = 13.64: IOTFm(4, 1) = 12.97
IOTFm(5, 0) = 4: IOTFm(5, 4) = 17.55: IOTFm(5, 5) = 19.29: IOTFm(5, 3) = 14.43: IOTFm(5, 2) = 13.52: IOTFm(5, 1) = 12.86
IOTFm(6, 0) = 4.5: IOTFm(6, 4) = 17.47: IOTFm(6, 5) = 19.26: IOTFm(6, 3) = 14.31: IOTFm(6, 2) = 13.41: IOTFm(6, 1) = 12.76
IOTFm(7, 0) = 5: IOTFm(7, 4) = 17.42: IOTFm(7, 5) = 19.3: IOTFm(7, 3) = 14.21: IOTFm(7, 2) = 13.31: IOTFm(7, 1) = 12.66
IOTFm(8, 0) = 5.5: IOTFm(8, 4) = 17.45: IOTFm(8, 5) = 19.47: IOTFm(8, 3) = 14.13: IOTFm(8, 2) = 13.22: IOTFm(8, 1) = 12.58
IOTFm(9, 0) = 6: IOTFm(9, 4) = 17.55: IOTFm(9, 5) = 19.78: IOTFm(9, 3) = 14.07: IOTFm(9, 2) = 13.15: IOTFm(9, 1) = 12.5
IOTFm(10, 0) = 6.5: IOTFm(10, 4) = 17.71: IOTFm(10, 5) = 20.23: IOTFm(10, 3) = 14.04: IOTFm(10, 2) = 13.1: IOTFm(10, 1) = 12.45
IOTFm(11, 0) = 7: IOTFm(11, 4) = 17.92: IOTFm(11, 5) = 20.63: IOTFm(11, 3) = 14.04: IOTFm(11, 2) = 13.08: IOTFm(11, 1) = 12.42
IOTFm(12, 0) = 7.5: IOTFm(12, 4) = 18.16: IOTFm(12, 5) = 21.09: IOTFm(12, 3) = 14.08: IOTFm(12, 2) = 13.09: IOTFm(12, 1) = 12.41
IOTFm(13, 0) = 8: IOTFm(13, 4) = 18.44: IOTFm(13, 5) = 21.6: IOTFm(13, 3) = 14.15: IOTFm(13, 2) = 13.11: IOTFm(13, 1) = 12.42
IOTFm(14, 0) = 8.5: IOTFm(14, 4) = 18.76: IOTFm(14, 5) = 22.17: IOTFm(14, 3) = 14.24: IOTFm(14, 2) = 13.17: IOTFm(14, 1) = 12.45
IOTFm(15, 0) = 9: IOTFm(15, 4) = 19.1: IOTFm(15, 5) = 22.77: IOTFm(15, 3) = 14.35: IOTFm(15, 2) = 13.24: IOTFm(15, 1) = 12.5
IOTFm(16, 0) = 9.5: IOTFm(16, 4) = 19.46: IOTFm(16, 5) = 23.39: IOTFm(16, 3) = 14.49: IOTFm(16, 2) = 13.34: IOTFm(16, 1) = 12.57
IOTFm(17, 0) = 10: IOTFm(17, 4) = 19.84: IOTFm(17, 5) = 24: IOTFm(17, 3) = 14.64: IOTFm(17, 2) = 13.45: IOTFm(17, 1) = 12.66
IOTFm(18, 0) = 10.5: IOTFm(18, 4) = 20.2: IOTFm(18, 5) = 24.57: IOTFm(18, 3) = 14.8: IOTFm(18, 2) = 13.58: IOTFm(18, 1) = 12.77
IOTFm(19, 0) = 11: IOTFm(19, 4) = 20.55: IOTFm(19, 5) = 25.1: IOTFm(19, 3) = 14.97: IOTFm(19, 2) = 13.72: IOTFm(19, 1) = 12.89
IOTFm(20, 0) = 11.5: IOTFm(20, 4) = 20.89: IOTFm(20, 5) = 25.58: IOTFm(20, 3) = 15.16: IOTFm(20, 2) = 13.87: IOTFm(20, 1) = 13.03
IOTFm(21, 0) = 12: IOTFm(21, 4) = 21.22: IOTFm(21, 5) = 26.02: IOTFm(21, 3) = 15.35: IOTFm(21, 2) = 14.05: IOTFm(21, 1) = 13.18
IOTFm(22, 0) = 12.5: IOTFm(22, 4) = 21.56: IOTFm(22, 5) = 26.43: IOTFm(22, 3) = 15.58: IOTFm(22, 2) = 14.25: IOTFm(22, 1) = 13.37
IOTFm(23, 0) = 13: IOTFm(23, 4) = 21.91: IOTFm(23, 5) = 26.84: IOTFm(23, 3) = 15.84: IOTFm(23, 2) = 14.48: IOTFm(23, 1) = 13.59
IOTFm(24, 0) = 13.5: IOTFm(24, 4) = 22.27: IOTFm(24, 5) = 27.25: IOTFm(24, 3) = 16.12: IOTFm(24, 2) = 14.74: IOTFm(24, 1) = 13.83
IOTFm(25, 0) = 14: IOTFm(25, 4) = 22.62: IOTFm(25, 5) = 27.63: IOTFm(25, 3) = 16.41: IOTFm(25, 2) = 15.01: IOTFm(25, 1) = 14.09
IOTFm(26, 0) = 14.5: IOTFm(26, 4) = 22.96: IOTFm(26, 5) = 27.98: IOTFm(26, 3) = 16.69: IOTFm(26, 2) = 15.28: IOTFm(26, 1) = 14.35
IOTFm(27, 0) = 15: IOTFm(27, 4) = 23.29: IOTFm(27, 5) = 28.3: IOTFm(27, 3) = 16.98: IOTFm(27, 2) = 15.55: IOTFm(27, 1) = 14.6
IOTFm(28, 0) = 15.5: IOTFm(28, 4) = 23.6: IOTFm(28, 5) = 28.6: IOTFm(28, 3) = 17.26: IOTFm(28, 2) = 15.82: IOTFm(28, 1) = 14.86
IOTFm(29, 0) = 16: IOTFm(29, 4) = 23.9: IOTFm(29, 5) = 28.88: IOTFm(29, 3) = 17.54: IOTFm(29, 2) = 16.08: IOTFm(29, 1) = 15.12
IOTFm(30, 0) = 16.5: IOTFm(30, 4) = 24.19: IOTFm(30, 5) = 29.14: IOTFm(30, 3) = 17.8: IOTFm(30, 2) = 16.34: IOTFm(30, 1) = 15.36
IOTFm(31, 0) = 17: IOTFm(31, 4) = 24.46: IOTFm(31, 5) = 29.41: IOTFm(31, 3) = 18.05: IOTFm(31, 2) = 16.58: IOTFm(31, 1) = 15.6
IOTFm(32, 0) = 17.5: IOTFm(32, 4) = 24.73: IOTFm(32, 5) = 29.7: IOTFm(32, 3) = 18.28: IOTFm(32, 2) = 16.8: IOTFm(32, 1) = 15.81
IOTFm(33, 0) = 18: IOTFm(33, 4) = 25: IOTFm(33, 5) = 30: IOTFm(33, 3) = 18.5: IOTFm(33, 2) = 17: IOTFm(33, 1) = 16
End Sub

Sub GetItemGest(mycob As ComboBox, n1 As Integer, n2 As Integer)
Dim i As Integer, tmp As String
'AddItems to measures or SDS cols
mycob.Clear
mycob.Style = 2
mycob.BoundColumn = 1
mycob.AddItem "Ignore"    'not use Gestation age
'For i = 1 To 256   'A - IV, total 256 columns,
For i = n1 To n2    '21/2/2005
    mycob.AddItem ColName(i)
Next i
End Sub

Sub getOkage2()
'13/9/2004 copy from getOkage and modify for keep age scale if change ref
'Dim i As Integer, k As Integer
'ReDim HWB(6), invHWB(6)

Select Case tUnit
    Case "yr", "year", "years"
         OkAge = 1
    Case "mo", "month", "months"
         OkAge = 1
    Case "wk", "week", "weeks"
         OkAge = 1
    Case "dy", "day", "days"
         OkAge = 1
    Case Else
         OkAge = 0: SaUnit = 0: CaUnit = 0
End Select

'remove the rest codes to getOKHWB on 17/8/2005

End Sub

Sub getOkCOV()

'2/4/2007 to check if the Ref contains covariates
Dim k As Long, kk As Variant, pos As Integer
k = Workbooks(DataFile).Names(tName).RefersToRange.Row

'15/5/2007 check if one or two covariates
Select Case k
    Case 10
         NumCov = 1
         Cov1Lab = Workbooks(DataFile).Sheets(DataRef).Cells(7, 1)
         pos = InStr(1, Cov1Lab, " ")
         If pos > 1 Then Cov1Title = Mid(Cov1Lab, 1, pos - 1) Else Cov1Title = Cov1Lab
         'Cov1Title = Mid(Cov1Lab, 1, InStr(1, Cov1Lab, " ") - 1)
    Case 12
         NumCov = 2
         Cov1Lab = Workbooks(DataFile).Sheets(DataRef).Cells(8, 1)
         pos = InStr(1, Cov1Lab, " ")
         If pos > 1 Then Cov1Title = Mid(Cov1Lab, 1, pos - 1) Else Cov1Title = Cov1Lab
         'Cov1Title = Mid(Cov1Lab, 1, InStr(1, Cov1Lab, " ") - 1)
         Cov2Lab = Workbooks(DataFile).Sheets(DataRef).Cells(9, 1)
         pos = InStr(1, Cov2Lab, " ")
         If pos > 1 Then Cov2Title = Mid(Cov2Lab, 1, pos - 1) Else Cov2Title = Cov2Lab
         'Cov2Title = Mid(Cov2Lab, 1, InStr(1, Cov2Lab, " ") - 1)
    Case Else
         NumCov = 0
End Select

End Sub

Sub getOkHWB()
'17/8/2005 move from getOKAge & getOKAge2 the common part
Dim i As Integer, k As Integer
ReDim HWB(6), invHWB(6)
OkWT = 0: WTat = 0
For i = 1 To NameUsed
    If UCase(mTitle(i)) = "HEIGHT" And UCase(mUnit(i)) = "CM" Then
       HWB(1) = i: invHWB(i) = 1
    End If
    If UCase(mTitle(i)) = "WEIGHT" Then
       WTat = i     '14/4/2003
       OkWT = 1
       If UCase(mUnit(i)) = "KG" Then
          HWB(2) = i: invHWB(i) = 2
       End If
    End If
    If UCase(mTitle(i)) = "BMI" And UCase(mUnit(i)) = "KGLM2" Then    '8/8/2007 KGM2->KGLM2
       HWB(3) = i: invHWB(i) = 3
    End If
    If UCase(mTitle(i)) = "HEAD" Then
       HWB(4) = i: invHWB(i) = 4
    End If
    If UCase(mTitle(i)) = "SITHT" And UCase(mUnit(i)) = "CM" Then  '16/8/2005
        HWB(5) = i: invHWB(i) = 5
    End If
    If UCase(mTitle(i)) = "LEGLN" And UCase(mUnit(i)) = "CM" Then   '16/8/2005
       HWB(6) = i: invHWB(i) = 6
    End If
Next i
OkHWB = 0: OKHSL = 0
If HWB(1) <> 0 And HWB(2) <> 0 And HWB(3) <> 0 Then
   RankHWB
   OkHWB = 1
   If HWB(5) <> 0 And HWB(6) <> 0 Then
      OKHSL = 3
      RankHSL OKHSL    'ht,wt,bmi, rank sitht legln
   Else
     If HWB(4) <> 0 Then RankHead  'ht,wt,bmi head
   End If
Else
   If HWB(1) <> 0 Then
      If HWB(2) <> 0 Then
         RankHW
         If HWB(5) <> 0 And HWB(6) <> 0 Then
            OKHSL = 2
            RankHSL OKHSL     'ht wt rank sitht and legln
         End If
      Else
         RankH
         If HWB(5) <> 0 And HWB(6) <> 0 Then
            OKHSL = 1
            RankHSL OKHSL    'ht, rank sitht and legln,
         End If
      End If
   Else
      If HWB(2) <> 0 Then
         RankW
      End If
   End If
End If

End Sub

   Sub GetUserName(err As Integer)
   
   '7/2/2005 remove as did not work on Mac and was not be used since
   
   'On Error GoTo E
   
   ''----------------also Tim Cole not the current user
   ''7/7/2003 copy code from #161394 of Microsoft Knoeledge Base Article
   '   ' Buffer size for the return string.
   '   Const lpnLength As Integer = 255

   '   ' Get return buffer space.
   '   Dim status As Integer

   '   ' For getting user information.
   '   Dim lpName, lpUserName As String

   '   ' Assign the buffer size constant to lpUserName.
   '   lpUserName = space$(lpnLength + 1)

   '   ' Get the log-on name of the person using product.
   '   status = WNetGetUser(lpName, lpUserName, lpnLength)  'does not work on Mac

   '   ' See whether error occurred.
   '   If status = NoError Then
   '      ' This line removes the null character. Strings in C are null-
   '      ' terminated. Strings in Visual Basic are not null-terminated.
   '      ' The null character must be removed from the C strings to be used
   '      ' cleanly in Visual Basic.
   '      lpUserName = Left$(lpUserName, InStr(lpUserName, Chr(0)) - 1)
   '      SaveFname = lpUserName   'HP added 7/7/1003
   '   Else

   '      ' An error occurred.
   '      'MsgBox "Unable to get the name."
   '      SaveFname = ""  '7/7/2003 HP add
   '      End
   '  End If

   '   ' Display the name of the person logged on to the machine.
   '   'MsgBox "The person logged on this machine is: " & lpUserName
'Exit Sub
'E:
'err = 1
   End Sub
                
Sub Auto_Open()

MakeMenu


End Sub

Function DateAge(BRange As Variant, MRange As Variant, tscale As String) As Variant
'2/12/2004 calc age from dates of birth & measurement
Dim tBir As Single, tMea As Single
On Error GoTo E
DateAge = unknown2
If IsMissing(BRange) Or IsMissing(MRange) Then GoTo E
'If BRange = "" Or MRange = "" Then
   'GoTo E
'Else
   'If (Not IsNumeric(BRange)) Or (Not IsNumeric(MRange)) Then GoTo E
'End If
Select Case tscale
    Case "yr", "years"   '24/7/2007 add years,months,weeks,days
         DateAge = DateDiff("d", BRange, MRange) / 365.25
    Case "mo", "months"
         DateAge = DateDiff("d", BRange, MRange) / 365.25 * 12
    Case "wk", "weeks"
         DateAge = DateDiff("d", BRange, MRange) / 7
    Case "dy", "days"
         DateAge = DateDiff("d", BRange, MRange)
End Select

'DateAge = RoundSigs(DateAge, 4)   '14/1/2005
'DateAge = Round(DateAge, 2)     '7/1/2005 for max of 2 decimals, Round function not available in Mac
'DateAge = Int(DateAge * 100 + 0.5) / 100 '22/3/2005, 9/11/2007 remove

Exit Function

E:
'MsgBox ("Problem in BMI"), 48, "LMSgrowth"  '10/9/2004 remove
End Function


Function Legnew(HtRange As Variant, StRange As Variant) As Variant
'17/8/2005
Dim st As Single, ht As Single
On Error GoTo E
Legnew = unknown2
If IsMissing(StRange) Or IsMissing(HtRange) Then GoTo E
If StRange = "" Or HtRange = "" Then
   GoTo E
Else
   If (Not IsNumeric(StRange)) Or (Not IsNumeric(HtRange)) Then GoTo E
End If
st = StRange
ht = HtRange
Legnew = ht - st
Exit Function
E:
'MsgBox ("Problem in Legnew"), 48, "LMSgrowth"
End Function

Sub OpenNewRf()

Dim err As Integer, pos As Integer, s As String
Application.ScreenUpdating = False
On Error GoTo E
CPU = Application.OperatingSystem
PS = Application.PathSeparator
If CPU = "Mac" Then ZoomSize = ZoomMac Else ZoomSize = ZoomPC
NewRf = 1
frmCreateRf.Show   '23/6/2009
If TypeName(ActiveWorkbook) = "Nothing" Then GoTo E  '24/6/2009 Nothing means not exist
s = ActiveWorkbook.Name
pos = InStr(1, s, ".")
If pos <> 0 Then Wname = Mid(s, 1, pos - 1) Else Wname = s   '12/1/2007 add if as Mac gives name without .xls
'frmCreateRf.Show   remove to above 23/6/2009
Application.ScreenUpdating = True   '23/6/2009
Exit Sub  '23/6/2009

E:
Wname = ""   '23/6/2009
Application.ScreenUpdating = True
End Sub
Sub OpenOldRf()

Dim err As Integer, pos As Integer, s As String
Application.ScreenUpdating = False
On Error GoTo E
CPU = Application.OperatingSystem
PS = Application.PathSeparator
If CPU = "Mac" Then ZoomSize = ZoomMac Else ZoomSize = ZoomPC
NewRf = 0
frmCreateRf.Show   '24/6/2009
If TypeName(ActiveWorkbook) = "Nothing" Then GoTo E  '24/6/2009 Nothing means not exist
s = ActiveWorkbook.Name
pos = InStr(1, s, ".")
If pos <> 0 Then Wname = Mid(s, 1, pos - 1) Else Wname = s   '12/1/2007 add if as Mac gives name without .xls
'frmCreateRf.Show  remove 24/6/2009
Application.ScreenUpdating = True   '24/6/2009
Exit Sub  '24/6/2009

E:
Wname = ""   '24/6/2009
Application.ScreenUpdating = True
End Sub
Sub OpenPref()
'29/11/2005 for decimals of sds output, copy from Open* and modified
'9/11/2007 remove the Preference from menu but keep frmPref in case
'Dim err As Integer
'Application.ScreenUpdating = False
'On Error GoTo E
'CPU = Application.OperatingSystem
'PS = Application.PathSeparator
'If CPU = "Mac" Then ZoomSize = ZoomMac Else ZoomSize = ZoomPC
'If NOpenRf < 1 Then
'   getExistingXY err
'   If err = 1 Then GoTo E
'   If NAgree = 0 Then ChkAgree err     '12/5/2006
'   If err = 1 Or NAgree = 0 Then GoTo E   '12/5/2006
'   ZPInit
'   ZPopen
'   NOpenRf = NOpenRf + 1
'End If
'frmPref.Show
'Application.ScreenUpdating = True
'Exit Sub

'E:
'Application.ScreenUpdating = True
End Sub

Sub RankH()
'17/8/2005
Dim k As Integer, n As Integer
n = 1
If HWB(1) <> n Then 'move height to the first
   k = HWB(1): HWB(1) = n: HWB(invHWB(n)) = k
   RankSwitch k, n
End If

End Sub

Sub RankHSL(nn As Integer)
'16/8/2005 re-order names, ht, sitht, legln ...
'if n = 1, sitht at the second , n=2, the 3rd and n=3, the 4th, n = OKHSL
Dim k As Integer, n As Integer
n = nn + 1
If HWB(5) <> n Then 'move sitht to the second
   k = HWB(5): HWB(5) = n: HWB(invHWB(n)) = k  '17/8/2005
   RankSwitch k, n  '17/8/2005
End If
n = n + 1
If HWB(6) <> n Then 'move legln to the third
   k = HWB(6): HWB(6) = n: HWB(invHWB(n)) = k
   RankSwitch k, n  '17/8/2005
End If

End Sub





Sub RankSwitch(k As Integer, n As Integer)
'17/8/2005
Dim s As String, kt As Integer
kt = invHWB(k): invHWB(k) = invHWB(n): invHWB(n) = kt
s = mName(k): mName(k) = mName(n): mName(n) = s
s = mTitle(k): mTitle(k) = mTitle(n): mTitle(n) = s
s = mUnit(k): mUnit(k) = mUnit(n): mUnit(n) = s
End Sub


Sub RankW()
'16/8/2005 re-order names for wt to the first
Dim k As Integer, n As Integer
n = 1
If HWB(2) <> n Then 'move weight to the first
   k = HWB(2): HWB(2) = n: HWB(invHWB(n)) = k    '17/8/2005
   RankSwitch k, n  '17/8/2005
   WTat = 1
End If

End Sub


Function RevSearch(ByVal Sname As String, ByVal sb As String) As Integer
'22/3/2005 Mac does not has InStrRev function, this function to replace it
RevSearch = 0
Do While InStr(Sname, sb)
   RevSearch = RevSearch + InStr(Sname, sb)
   Sname = Right(Sname, Len(Sname) - InStr(Sname, sb))
Loop
End Function

Function RoundSigs(num As Variant, sigs As Variant)
'11/1/2005 copy from http://www.vertex42.com/ExcelTips/significant-figures.html
'=ROUND(value,sigfigs-(1+INT(LOG10(ABS(value)))))
'value :: the number you wish to round.
'sigfigs :: the number of significant figures you want to round to.

'29/11/2005 copy another function, see Function FormatSF

    Dim exponent As Double
    If IsNumeric(num) And IsNumeric(sigs) Then
        If sigs < 1 Then
            ' Return the  " #NUM "  error
            RoundSigs = CVErr(xlErrNum)
        Else
            exponent = Int(Log(Abs(num)) / Log(10#))
            RoundSigs = WorksheetFunction.Round(num, _
                       sigs - (1 + exponent))
        End If
    Else
        ' Return the  " #N/A "  error
        RoundSigs = CVErr(xlErrNA)
    End If
End Function
'Returns input number rounded to specified number of significant figures.
Function FormatSF(dblInput As Double, intSF As Integer) As String

Dim intCorrPower As Integer         'Exponent used in rounding calculation
Dim intSign As Integer              'Holds sign of dblInput since logs are used in calculations

'-- Store sign of dblInput --
intSign = Sgn(dblInput)

'-- Calculate exponent of dblInput --
'intCorrPower = Int(Log10(Abs(dblInput)))  'use log10(x) function in original codes
intCorrPower = Int(Log(Abs(dblInput)) / Log(10#))  'I changed to avoid using log10(x) on 29/11/2005

FormatSF = Round(dblInput * 10 ^ ((intSF - 1) - intCorrPower))   'integer value with no sig fig
FormatSF = FormatSF * 10 ^ (intCorrPower - (intSF - 1))         'raise to original power


'-- Reconsitute final answer --
FormatSF = FormatSF * intSign

'-- Answer sometimes needs padding with 0s --
If InStr(FormatSF, ".") = 0 Then
    If Len(FormatSF) < intSF Then
        FormatSF = Format(FormatSF, "##0." & String(intSF - Len(FormatSF), "0"))
    End If
End If

If intSF > 1 And Abs(FormatSF) < 1 Then
    Do Until Left(Right(FormatSF, intSF), 1) <> "0" And Left(Right(FormatSF, intSF), 1) <> "."
        FormatSF = FormatSF & "0"
    Loop
End If
''Calculate Log to the Base 10 see Function log10(x)
'Function Log10(x)
   'Log10 = Log(x) / Log(10#)
'End Function


End Function




Sub Auto_Close()

DeleteMenu   '28/5/2003
End Sub
Function getlblSDS(Fidx As Integer) As String
'22/6/2007 ,remove 3/8/2007
'Dim s As String, i As Integer
's = FNClist(Fidx)
'For i = 1 To 7 - Int(Len(s) / 2)
'   s = " " & s
'Next i
'getlblSDS = s
End Function
Function zLMS(Y As Single, LL As Single, MM As Single, SS As Single) As Single
'21/6/2007
If LL = 1 Then
   zLMS = (Y / MM - 1) / SS
Else
   If LL <> 0 Then
      zLMS = (Exp(LL * (Log(Y / MM))) - 1) / (LL * SS)  'not VBA's log = Excel's =Application.LN
   Else
      zLMS = (Log(Y / MM)) / SS
   End If
End If

End Function

Sub ZPInit()
'14/12/2004 copy from LMS and modify
Dim i As Long
'default for unequal space
NcentU = 7
porz = 1
Puequal = "3;10;25;50;75;90;97"    '17/3/2005
Zuequal = "-2;-1;0;1;2"            '17/3/2005 may use "-1.881;-1.2816;...."
'equal space
nequal = 1
NcentE = 7
Ncent = NcentE
space = 2 / 3  '0.6667

End Sub


Sub ZPopen()
'14/12/2004 if error occur then use default in ZPinit

Dim fname As String, s As String, i As Integer, tmpe As Single, tmpne As Integer, tmpn As Integer, tmpor As Integer
On Error GoTo E
fname = PathRoot & "prevsds"    '11/2/2005
If Dir(fname) = "" Then Exit Sub
Open fname For Input As 1  ' Open file selected on File Open About.
Do Until EOF(1)
Line Input #1, s
If IsNumeric(s) = False Then GoTo E Else tmpne = CInt(s)   'nequal
If tmpne <> 0 And tmpne <> 1 Then GoTo E  '1/3/2001
Line Input #1, s
If IsNumeric(s) = False Then GoTo E Else tmpn = CInt(s)    'ncent
If tmpn < 1 Or tmpn > 30 Then GoTo E
Select Case tmpne
    Case 0  'not equal
         Line Input #1, s  '17/3/2005
         If IsNumeric(s) = False Then GoTo E Else tmpor = CInt(s)   'porz
         If tmpor <> 1 And tmpor <> 2 Then GoTo E
         Line Input #1, s
         If s = "" Then GoTo E
    Case 1   'equal
         Line Input #1, s
         If IsNumeric(s) = False Then
            GoTo E
         Else
            tmpe = CSng(s)
            If tmpe < 0 Then GoTo E
         End If
End Select
Loop
Close 1  ' Close file
Select Case tmpne
     Case 0
         Ncent = tmpn: NcentU = tmpn: porz = tmpor
         If porz = 1 Then
            Puequal = s         'Zuequal uses "-2;-1;0;1;2" as default
         Else
            Zuequal = s         'Puequal uses "3;10;25;50;75;90;97" as default
         End If
      Case 1
         Ncent = tmpn: NcentE = tmpn: space = tmpe
End Select
nequal = tmpne
E:
    Close 1
End Sub

Function BMInew(WtRange As Variant, HtRange As Variant) As Variant
'copy from BMI and modify for flexible on 1/5/2003
Dim wt As Single, ht As Single
On Error GoTo E
BMInew = unknown2
If IsMissing(WtRange) Or IsMissing(HtRange) Then GoTo E
If WtRange = "" Or HtRange = "" Then
   GoTo E 'dd->E 10/9/2004
Else
   If (Not IsNumeric(WtRange)) Or (Not IsNumeric(HtRange)) Then GoTo E
End If
'need multiple by rate for WtRange & HtRange
wt = WtRange  'kg
ht = HtRange / 100   'cm->m
BMInew = wt / ht / ht
'BMInew = Int(BMInew * 100 + 0.5) / 100    'remove 9/11/2007

Exit Function

E:
'MsgBox ("Problem in BMI"), 48, "LMSgrowth"  '10/9/2004 remove
End Function


Sub CalcBMInew(indexHT1 As Integer, indexwt1 As Integer, indexBMI As Integer, indexHead As Integer, row1 As Long, row2 As Long)
'copy from CalBMI & modify for flexible version on 1/5/2003

Dim i As Long, cur As String, j1 As Integer, j2 As Integer, tmprow1 As Long
'On Error Resume Next
On Error GoTo E
Application.ScreenUpdating = False

cur = ColName(indexBMI)
SetColFormat cur        '9/11/2007
j1 = indexwt1 - indexBMI
j2 = indexHT1 - indexBMI
If indexHead = 1 Then  'for *_I & *_S
   tmprow1 = row1 + 1
   Range(cur & row1).value = "BMI"
Else
   tmprow1 = row1
End If

For i = tmprow1 To row2   '13/7/2005
    Range(cur & i).Select
    ActiveCell.FormulaR1C1 = "=BMInew(RC[" & j1 & "],RC[" & j2 & "])"
Next i
Application.ScreenUpdating = True
Exit Sub
E:
'MsgBox ("Problem in CalcBMI"), 48, "LMSgrowth"  '10/9/2004 remove

End Sub





Sub CalcCentile(iSex As Integer)
' 17/11/2004 use centYMWD i, 4/3/2005 add iSex
On Error GoTo E

Dim i As Integer
For i = 1 To MaxN   '4/3/2005
    If idxM3_s(i) = 1 Then CentYMWD i, iSex
Next i
Exit Sub

E:
'MsgBox "problem in CalcCentile", 48, "LMSgrowth"   '10/9/2004 remove

End Sub


Sub CalcSDS(iSex As Integer)
' 17/11/2004 use SDSYMWD i, 4/3/2005 add iSex
On Error GoTo E

Dim i As Integer

For i = 1 To MaxN   '4/3/2005
    If idxM3_s(i) = 1 Then SDSYMWD i, iSex   '4/3/2005
Next i
Exit Sub

E:
'MsgBox "problem in CalcSDS", 48, "LMSgrowth"  '10/9/2004 remove
End Sub
Sub CalcSD(iSex As Integer)
' 24/7/2007 copy from CalcSDS
On Error GoTo E

Dim i As Integer

For i = 1 To MaxN
    'If idxM3_s(i) = 1 Then SDYMWD i, iSex
    If Fidx > 3 Or (Fidx < 4 And idxM3_s(i) = 1) Then SDYMWD i, iSex      '20/4/2011
Next i
Exit Sub

E:
'MsgBox "problem in CalcSD", 48, "LMSgrowth"
End Sub

Sub CalcFNC(iSex As Integer)
' 21/6/2007 copy SDSYMWD and modify for Lung
On Error GoTo E

Dim i As Integer
For i = 1 To MaxN   '4/3/2005
    'If idxM3_c(i) = 1 Then FNCYMWD i, iSex   '4/3/2005
    If Fidx > 3 Or (Fidx < 4 And idxM3_c(i) = 1) Then FNCYMWD i, iSex      '20/4/2011
Next i
Exit Sub

E:
'MsgBox "problem in CalcSDS", 48, "LMSgrowth"  '10/9/2004 remove
End Sub









Sub OpenZP()
'13/12/2004
Dim err As Integer
'err = 0
Application.ScreenUpdating = False
On Error GoTo E
CPU = Application.OperatingSystem
PS = Application.PathSeparator
If CPU = "Mac" Then ZoomSize = ZoomMac Else ZoomSize = ZoomPC
If NOpenRf < 1 Then
   getExistingXY err
   If err = 1 Then GoTo E
   ZPInit     '16/5/2005
   ZPopen     '16/5/2005
   NOpenRf = NOpenRf + 1
End If
If NumCov = 0 Then frmZP.Show Else MsgBox ("Calculation of centiles is not available for the selected references."), 48, "LMSgrowth"   '15/5/2007
'frmZP.Show
Application.ScreenUpdating = True
Exit Sub

E:
Application.ScreenUpdating = True
End Sub

Sub WtGainYMWD(iSex As Integer)
'16/5/2003, modify on 23/11/2004, 1/2/2005
Dim j1 As Integer, j2 As Integer, j3 As Integer, j4 As Integer, j5 As Integer, cur As String, s1 As String, s2 As String
Dim tmpName As String, tmps1 As String, tmps2 As String, tmpDfile As String, tmpaName As String, DatRow1_g_adj As Long    '1/2/2005
Dim tmpDAgeU1 As String, tmpDAgeU2 As String    '8/3/2005
'On Error Resume Next
On Error GoTo E
cur = ColName(idxSDS_g)   'use 256 columns
SetColFormat cur        '9/11/2007
If NHead_g = 1 Then   '1/2/2005
   DatRow1_g_adj = DatRow1_g + 1
   Range(cur & DatRow1_g).value = "SDS_WtGain"   '4/3/2005
Else
   DatRow1_g_adj = DatRow1_g
End If
If DatRow1_g_adj > DatRow2_g Then Exit Sub
'cur = ColName(idxSDS_g)   'use 256 columns, 4/3/2005 move to top
'Application.ScreenUpdating = False
j1 = idxAge1_g - idxSDS_g
j2 = idxWT1_g - idxSDS_g
j3 = idxAge2_g - idxSDS_g
j4 = idxWT2_g - idxSDS_g
j5 = idxSex_g - 1 - idxSDS_g
s1 = AgeScale(idxSc1_g + 1)
s2 = AgeScale(idxSc2_g + 1)
cur = ColName(idxSDS_g)   'use 256 columns
Range(cur & DatRow1_g_adj).Select   '1/2/2005
tmpName = Chr(34) & mName(WTat) & Chr(34)   '22/11/2004
tmps1 = Chr(34) & s1 & Chr(34)              '23/11/2004  for "y", "m", "w", "d" as required by Tim's old function for wtgain
tmps2 = Chr(34) & s2 & Chr(34)              '23/11/2004  for "y", "m", "w", "d"
tmpDfile = Chr(34) & DataFile & Chr(34)     '23/11/2004
tmpaName = Chr(34) & tName & Chr(34)  '29/11/2004 for tname
tmpDAgeU1 = Chr(34) & frmWtGainCo!cobSc1.Text & Chr(34)     '8/3/2005
tmpDAgeU2 = Chr(34) & frmWtGainCo!cobSc2.Text & Chr(34)     '8/3/2005
Dim Ssex As Variant  '4/3/2005
Select Case iSex     '4/3/2005
   Case 0
        Ssex = Chr(34) & "M" & Chr(34)
   Case 1
        Ssex = Chr(34) & "F" & Chr(34)
   Case Is > 1
        Ssex = "RC[" & j5 & "]"
End Select
ActiveCell.FormulaR1C1 = "=cSDSGAIN(RC[" & j1 & "], " & tmps1 & " ,cSDS(" & Ssex & ",RC[" & j1 & "]," & tmpDAgeU1 & ",RC[" & j2 & "]," & tmpaName & "," & tmpName & ", " & tmpDfile & "),RC[" & j3 & "], " & tmps2 & " ,cSDS(" & Ssex & ",RC[" & j3 & "]," & tmpDAgeU2 & ",RC[" & j4 & "]," & tmpaName & "," & tmpName & ", " & tmpDfile & "))"
'ActiveCell.FormulaR1C1 = "=cSDSGAIN(RC[" & j1 & "], " & tmps1 & " ,cSDS(RC[" & j5 & "],RC[" & j1 & "]," & AgeR_g1 & ",RC[" & j2 & "]," & tmpaName & "," & tmpName & ", " & tmpDfile & "),RC[" & j3 & "], " & tmps2 & " ,cSDS(RC[" & j5 & "],RC[" & j3 & "]," & AgeR_g2 & ",RC[" & j4 & "]," & tmpaName & "," & tmpName & ", " & tmpDfile & "))"
If DatRow2_g > DatRow1_g_adj Then   '1/2/2005
   Range(cur & DatRow1_g_adj).Select
   Selection.AutoFill Destination:=Range(cur & DatRow1_g_adj & ":" & cur & DatRow2_g), Type:=xlFillDefault
End If
'Application.ScreenUpdating = True
Exit Sub
E:
'MsgBox "problem in WtGainYMWD", 48, "LMSgrowth"   '10/9/2004 remove
End Sub










































Sub ChkRefOpen(Data As String, err As Integer)
Dim msg As String
On Error GoTo E
err = 0
If IsBookOpen(Data) = False Then
   If Not IsDiskFile(Data) Then
      GoTo E
   Else
      Workbooks.Open Data
   End If
End If
Exit Sub
E:
err = 1
End Sub






Function cIOTF(sexRange As Variant, tRange As Variant, DAgeU As String, Yrange As Variant) As Variant

Dim tmin As Single, tmax As Single, cols As Integer, t As Single, Y As Single
Dim overwt As Single, obesity As Single, k As Long, ScrFail As Integer
Dim AgeR As Single, RAgeU As String, Nm As Integer   '8/3/2005

'On Error Resume Next
On Error GoTo E
cIOTF = unknown
'check sex
If sexRange = "" Then GoTo E
If (Not IsNumeric(sexRange)) Then
    If UCase(Trim(sexRange)) = "M" Or UCase(Trim(sexRange)) = "MALE" Then   '17/8/2005
       cols = 2
    Else
       If UCase(Trim(sexRange)) = "F" Or UCase(Trim(sexRange)) = "FEMALE" Then   '17/8/2005
          cols = 4
       Else
          GoTo E
       End If
    End If
Else
    If sexRange = 1 Then
       cols = 2
    Else
       If sexRange = 2 Then
          cols = 4
        Else
          GoTo E
        End If
    End If
End If
'Check age
If IsMissing(tRange) = True Then GoTo E
If tRange = "" Then GoTo E
If (Not IsNumeric(tRange)) Then GoTo E
tmin = IOTFRf(1, 0)   '2 to 18 step 0.5
tmax = IOTFRf(33, 0)
RAgeU = "yr"
getAgeRate DAgeU, RAgeU, AgeR   '8/3/2005
t = tRange * AgeR  '3/2/2005
If (t < tmin) Or (t > tmax) Then GoTo E
'check yy
If IsMissing(Yrange) Then GoTo E
If Yrange = "" Then GoTo E
If (Not IsNumeric(Yrange)) Then GoTo E

Y = Yrange
If Y <= 0 Then GoTo E
BinarySearchI t, cols, overwt, obesity, ScrFail
If ScrFail = 1 Then GoTo E '15/9/2004 Age out of range

If Y < overwt Then
   cIOTF = 0
Else
   If Y >= obesity Then cIOTF = 2 Else cIOTF = 1
End If

Exit Function
E:
'MsgBox "problem in cIOTF", 48, "LMSgrowth"   'remove 15/9/2004

End Function
Function cIOTF2(sexRange As Variant, tRange As Variant, DAgeU As String, Yrange As Variant) As Variant
'23/04/2007 copy cIOTF and modified to add thinness, keep cIOTF for old versions
Dim tmin As Single, tmax As Single, cols As Integer, t As Single, Y As Single
Dim overwt As Single, obesity As Single, k As Long, ScrFail As Integer
Dim AgeR As Single, RAgeU As String, Nm As Integer   '8/3/2005
Dim Nsex As Integer, cutoff(5) As Single   '23/4/2007

'On Error Resume Next
On Error GoTo E
cIOTF2 = unknown
'check sex
If sexRange = "" Then GoTo E
If (Not IsNumeric(sexRange)) Then
    If UCase(Trim(sexRange)) = "M" Or UCase(Trim(sexRange)) = "MALE" Then   '17/8/2005
       Nsex = 1
    Else
       If UCase(Trim(sexRange)) = "F" Or UCase(Trim(sexRange)) = "FEMALE" Then   '17/8/2005
          Nsex = 2
       Else
          GoTo E
       End If
    End If
Else
    If sexRange = 1 Then
       Nsex = 1
    Else
       If sexRange = 2 Then
          Nsex = 2
        Else
          GoTo E
        End If
    End If
End If
'Check age
If IsMissing(tRange) = True Then GoTo E
If tRange = "" Then GoTo E
If (Not IsNumeric(tRange)) Then GoTo E
tmin = IOTFm(1, 0)   '2 to 18 step 0.5, age same in sex
tmax = IOTFm(33, 0)
RAgeU = "yr"
getAgeRate DAgeU, RAgeU, AgeR   '8/3/2005
t = tRange * AgeR  '3/2/2005
If (t < tmin) Or (t > tmax) Then GoTo E
'check yy
If IsMissing(Yrange) Then GoTo E
If Yrange = "" Then GoTo E
If (Not IsNumeric(Yrange)) Then GoTo E
Y = Yrange
If Y <= 0 Then GoTo E

If Nsex = 1 Then BinarySearch2 t, Nsex, IOTFm(), cutoff(), ScrFail Else BinarySearch2 t, Nsex, IOTFf(), cutoff(), ScrFail
If ScrFail = 1 Then GoTo E
'cIOTF = 3,2,0,-1,-2,-3 if >=30, >=25&<30, >=18.5&<25, >=17&<18.5, >=16&<17, <16
If Y >= cutoff(5) Then
   cIOTF2 = 2
ElseIf Y < cutoff(5) And Y >= cutoff(4) Then
   cIOTF2 = 1
ElseIf Y < cutoff(4) And Y >= cutoff(3) Then
   cIOTF2 = 0
ElseIf Y < cutoff(3) And Y >= cutoff(2) Then
   cIOTF2 = -1
ElseIf Y < cutoff(2) And Y >= cutoff(1) Then
   cIOTF2 = -2
ElseIf Y < cutoff(1) Then
   cIOTF2 = -3
End If
cIOTF2 = cIOTF2
Exit Function
E:
'MsgBox "problem in cIOTF2", 48, "LMSgrowth"   'remove 15/9/2004

End Function

Sub getExistingXY(err As Integer)
'get names from saved file prevrfn for the first open of a ref
Dim tmpF As String, s As String, FileNumber As Integer, i As Integer, n As Integer, Nx As Integer, Ny As Integer, tmpDataFile As String, agname As String
On Error GoTo E 'if British 1990 not available
err = 0
RfPath = Workbooks("British1990.xls").Path   '24/11/2004 if not exist goto E
getPathRoot err
If err = 1 Then GoTo E  'error not installed British1990
'GetUserName err   '7/7/2003  to get SaveFname work on PC not MAc
DataFile = "BRITISH1990.XLS"    'move from bottom 16/5/2005 get default first
DataRef = "British1990"
getDefXYused                    'move from bottom 16/5/2005

On Error GoTo E2    'use default British 1990
SaveFname = PathRoot & "prevrfn"    '5/6/2003
s = Dir(SaveFname)
If s <> "" Then    '4/7/2003 if read sucessfully use saved one else use default
   FileNumber = FreeFile
   Open SaveFname For Input As #FileNumber   '4/7/2003
   Line Input #FileNumber, s
   tmpDataFile = Trim(s)    '17/5/2005
   ChkRefOpen tmpDataFile, err  'if pre-seleced ref open   '17/5/2005
   If err = 1 Then
      err = 0: GoTo E2   'd1->E 16/5/2005  'use default
   End If
   Dim tmpn As Integer, SS As String, tmptname As String, tmptTitle As String, tmptunit As String, k As Integer
   Dim tmpmName(20) As String, tmpmUnit(20) As String, tmpmTitle(20) As String
   Line Input #FileNumber, s
   tmpn = CInt(s)
   Nx = 0: Ny = 0
   For i = 1 To tmpn
       Line Input #FileNumber, s
       SS = Mid(s, 1, 2)
       If SS = "X_" Or SS = "x_" Then
          n = InStr(3, s, "_", 1)
          If n < 4 Or n = Len(s) Then GoTo E2 'd1->E 16/5/2005, E2 on 25/5/2005
          tmptname = s
          tmptTitle = Mid(s, 3, n - 3)
          tmptunit = Mid(s, n + 1, Len(s) - n)
          Nx = Nx + 1
       End If
       If SS = "Y_" Or SS = "y_" Then
          n = InStr(3, s, "_", 1)
          If n < 4 Or n = Len(s) Then GoTo E2    'd1->E 16/5/2005, E2 on 25/5/2005
          Ny = Ny + 1
          tmpmName(Ny) = s
          tmpmTitle(Ny) = Mid(s, 3, n - 3)
          tmpmUnit(Ny) = Mid(s, n + 1, Len(s) - n)
       End If
   Next i
   If Nx <> 1 Or Ny > MaxN Or Ny < 1 Then GoTo E2   'd1->E 16/5/2005, E2 on 25/5/2005   'MaxN names in dialogues
   ReDim mTitle(MaxN) As String, mName(MaxN) As String, mUnit(MaxN) As String
   NameUsed = Ny
   DataFile = tmpDataFile    '17/5/2005
   DataRef = Mid(tmpDataFile, 1, Len(tmpDataFile) - 4)   '17/5/2005
   tName = tmptname: tTitle = tmptTitle: tUnit = LCase(tmptunit)
   For i = 1 To Ny  'for selected names by last run
       mName(i) = tmpmName(i): mTitle(i) = tmpmTitle(i): mUnit(i) = tmpmUnit(i)
   Next i
   getOkAge   '23/6/2003
   getOkHWB   '17/8/2005
   getOkCOV   '2/4/2007
   Close #FileNumber
End If
Exit Sub   '4/7/2003
E:
err = 1  'remove 16/5/2005
MsgBox "British1990 is not available.", 48, "LMSgrowth"   '16/5/2005 British1990
E2:
Close #FileNumber
End Sub


Sub getIOTFRf()
'2/7/2003
'0-t, 1-boy overwt, 2-boy obesity, 3-girl overwt, 4-girl obesity
IOTFRf(1, 0) = 2: IOTFRf(1, 1) = 18.41: IOTFRf(1, 2) = 20.09: IOTFRf(1, 3) = 18.02: IOTFRf(1, 4) = 19.81
IOTFRf(2, 0) = 2.5: IOTFRf(2, 1) = 18.13: IOTFRf(2, 2) = 19.8: IOTFRf(2, 3) = 17.76: IOTFRf(2, 4) = 19.55
IOTFRf(3, 0) = 3: IOTFRf(3, 1) = 17.89: IOTFRf(3, 2) = 19.57: IOTFRf(3, 3) = 17.56: IOTFRf(3, 4) = 19.36
IOTFRf(4, 0) = 3.5: IOTFRf(4, 1) = 17.69: IOTFRf(4, 2) = 19.39: IOTFRf(4, 3) = 17.4: IOTFRf(4, 4) = 19.23
IOTFRf(5, 0) = 4: IOTFRf(5, 1) = 17.55: IOTFRf(5, 2) = 19.29: IOTFRf(5, 3) = 17.28: IOTFRf(5, 4) = 19.15
IOTFRf(6, 0) = 4.5: IOTFRf(6, 1) = 17.47: IOTFRf(6, 2) = 19.26: IOTFRf(6, 3) = 17.19: IOTFRf(6, 4) = 19.12
IOTFRf(7, 0) = 5: IOTFRf(7, 1) = 17.42: IOTFRf(7, 2) = 19.3: IOTFRf(7, 3) = 17.15: IOTFRf(7, 4) = 19.17
IOTFRf(8, 0) = 5.5: IOTFRf(8, 1) = 17.45: IOTFRf(8, 2) = 19.47: IOTFRf(8, 3) = 17.2: IOTFRf(8, 4) = 19.34
IOTFRf(9, 0) = 6: IOTFRf(9, 1) = 17.55: IOTFRf(9, 2) = 19.78: IOTFRf(9, 3) = 17.34: IOTFRf(9, 4) = 19.65
IOTFRf(10, 0) = 6.5: IOTFRf(10, 1) = 17.71: IOTFRf(10, 2) = 20.23: IOTFRf(10, 3) = 17.53: IOTFRf(10, 4) = 20.08
IOTFRf(11, 0) = 7: IOTFRf(11, 1) = 17.92: IOTFRf(11, 2) = 20.63: IOTFRf(11, 3) = 17.75: IOTFRf(11, 4) = 20.51
IOTFRf(12, 0) = 7.5: IOTFRf(12, 1) = 18.16: IOTFRf(12, 2) = 21.09: IOTFRf(12, 3) = 18.03: IOTFRf(12, 4) = 21.01
IOTFRf(13, 0) = 8: IOTFRf(13, 1) = 18.44: IOTFRf(13, 2) = 21.6: IOTFRf(13, 3) = 18.35: IOTFRf(13, 4) = 21.57
IOTFRf(14, 0) = 8.5: IOTFRf(14, 1) = 18.76: IOTFRf(14, 2) = 22.17: IOTFRf(14, 3) = 18.69: IOTFRf(14, 4) = 22.18
IOTFRf(15, 0) = 9: IOTFRf(15, 1) = 19.1: IOTFRf(15, 2) = 22.77: IOTFRf(15, 3) = 19.07: IOTFRf(15, 4) = 22.81
IOTFRf(16, 0) = 9.5: IOTFRf(16, 1) = 19.46: IOTFRf(16, 2) = 23.39: IOTFRf(16, 3) = 19.45: IOTFRf(16, 4) = 23.46
IOTFRf(17, 0) = 10: IOTFRf(17, 1) = 19.84: IOTFRf(17, 2) = 24: IOTFRf(17, 3) = 19.86: IOTFRf(17, 4) = 24.11
IOTFRf(18, 0) = 10.5: IOTFRf(18, 1) = 20.2: IOTFRf(18, 2) = 24.57: IOTFRf(18, 3) = 20.29: IOTFRf(18, 4) = 24.77
IOTFRf(19, 0) = 11: IOTFRf(19, 1) = 20.55: IOTFRf(19, 2) = 25.1: IOTFRf(19, 3) = 20.74: IOTFRf(19, 4) = 25.42
IOTFRf(20, 0) = 11.5: IOTFRf(20, 1) = 20.89: IOTFRf(20, 2) = 25.58: IOTFRf(20, 3) = 21.2: IOTFRf(20, 4) = 26.05
IOTFRf(21, 0) = 12: IOTFRf(21, 1) = 21.22: IOTFRf(21, 2) = 26.02: IOTFRf(21, 3) = 21.68: IOTFRf(21, 4) = 26.67
IOTFRf(22, 0) = 12.5: IOTFRf(22, 1) = 21.56: IOTFRf(22, 2) = 26.43: IOTFRf(22, 3) = 22.14: IOTFRf(22, 4) = 27.24
IOTFRf(23, 0) = 13: IOTFRf(23, 1) = 21.91: IOTFRf(23, 2) = 26.84: IOTFRf(23, 3) = 22.58: IOTFRf(23, 4) = 27.76
IOTFRf(24, 0) = 13.5: IOTFRf(24, 1) = 22.27: IOTFRf(24, 2) = 27.25: IOTFRf(24, 3) = 22.98: IOTFRf(24, 4) = 28.2
IOTFRf(25, 0) = 14: IOTFRf(25, 1) = 22.62: IOTFRf(25, 2) = 27.63: IOTFRf(25, 3) = 23.34: IOTFRf(25, 4) = 28.57
IOTFRf(26, 0) = 14.5: IOTFRf(26, 1) = 22.96: IOTFRf(26, 2) = 27.98: IOTFRf(26, 3) = 23.66: IOTFRf(26, 4) = 28.87
IOTFRf(27, 0) = 15: IOTFRf(27, 1) = 23.29: IOTFRf(27, 2) = 28.3: IOTFRf(27, 3) = 23.94: IOTFRf(27, 4) = 29.11
IOTFRf(28, 0) = 15.5: IOTFRf(28, 1) = 23.6: IOTFRf(28, 2) = 28.6: IOTFRf(28, 3) = 24.17: IOTFRf(28, 4) = 29.29
IOTFRf(29, 0) = 16: IOTFRf(29, 1) = 23.9: IOTFRf(29, 2) = 28.88: IOTFRf(29, 3) = 24.37: IOTFRf(29, 4) = 29.43
IOTFRf(30, 0) = 16.5: IOTFRf(30, 1) = 24.19: IOTFRf(30, 2) = 29.14: IOTFRf(30, 3) = 24.54: IOTFRf(30, 4) = 29.56
IOTFRf(31, 0) = 17: IOTFRf(31, 1) = 24.46: IOTFRf(31, 2) = 29.41: IOTFRf(31, 3) = 24.7: IOTFRf(31, 4) = 29.69
IOTFRf(32, 0) = 17.5: IOTFRf(32, 1) = 24.73: IOTFRf(32, 2) = 29.7: IOTFRf(32, 3) = 24.85: IOTFRf(32, 4) = 29.84
IOTFRf(33, 0) = 18: IOTFRf(33, 1) = 25: IOTFRf(33, 2) = 30: IOTFRf(33, 3) = 25: IOTFRf(33, 4) = 30

End Sub

Sub getItemdat(mycob As ComboBox)
'25/3/2002 get item for format of date as Excel 97 does not recognize International setting for date
mycob.Clear
mycob.Style = 2
mycob.BoundColumn = 1
mycob.AddItem "dd/mm/yyyy"
mycob.AddItem "mm/dd/yyyy"
mycob.AddItem "yyyy-mm-dd"   '23/2/2005
End Sub

Sub getItemSca(mycob As ComboBox)
'get items for age scale in frmWtGain
mycob.Clear
mycob.Style = 2
mycob.BoundColumn = 1
mycob.AddItem "yr"     '8/3/2005  was "Years"
mycob.AddItem "mo"     '"Months"
mycob.AddItem "wk"     '"Weeks"
mycob.AddItem "dy"     '"Days"

End Sub

Sub GetItemSex(mycob As ComboBox, n1 As Integer, n2 As Integer)
Dim i As Integer, tmp As String
'AddItems to measures or SDS cols
mycob.Clear
mycob.Style = 2
mycob.BoundColumn = 1
mycob.AddItem "Male"    'listIndex = 0
mycob.AddItem "Female"
'For i = 1 To 256   'A - IV, total 256 columns, remove 1 to 256 21/2/2005
For i = n1 To n2   '21/2/2005
    mycob.AddItem ColName(i)
Next i
End Sub









Sub getOkAge()

'23/6/2003, 21/6/2007 add CaUnit
'Dim i As Integer, k As Integer
'ReDim HWB(6), invHWB(6)
Select Case tUnit 'in reference
    Case "yr", "year", "years"
         OkAge = 1: SaUnit = 1: CaUnit = 1
         IaUnit = 1: IaUnit_o = 1
         idxSc1_g = 0: idxSc2_g = 0: idxSc1_g_o = 0: idxSc2_g_o = 0  'wtgain
    Case "mo", "month", "months"
         OkAge = 1: SaUnit = 2: CaUnit = 2
         IaUnit = 2: IaUnit_o = 2
         idxSc1_g = 1: idxSc2_g = 1: idxSc1_g_o = 1: idxSc2_g_o = 1
    Case "wk", "week", "weeks"
         OkAge = 1: SaUnit = 3: CaUnit = 3
         IaUnit = 3: IaUnit_o = 3
         idxSc1_g = 2: idxSc2_g = 2: idxSc1_g_o = 2: idxSc2_g_o = 2
    Case "dy", "day", "days"
         OkAge = 1: SaUnit = 4: CaUnit = 4
         IaUnit = 4: IaUnit_o = 4
         idxSc1_g = 3: idxSc2_g = 3: idxSc1_g_o = 3: idxSc2_g_o = 3
    Case Else 'unknow age scale as unit
         OkAge = 0: SaUnit = 0: CaUnit = 0
         IaUnit = 0: IaUnit_o = 0   '14/9/2004 default as year in frmIOTF
        'if Okage = 0 do not load frmWTgain as can not convert unknown age scale that used for sds of wt to weeks that need in get SDS for wtgain
End Select
'remove the rest codes to getOKHWB on 17/8/2005

End Sub
Sub getPathRoot(err As Integer)
'2/6/2003
Dim Message As String, username As String, s As String, k As Integer
PathRoot = ""
On Error GoTo E
If CPU = "Mac" Then   '4/7/2003
   If InStr(1, UCase(RfPath), "STARTUP") <= 0 Then GoTo E
Else
   If InStr(1, UCase(RfPath), "XLSTART") <= 0 Then GoTo E
End If

k = InStr(1, UCase(RfPath), ":")
If k <= 0 Then
   PathRoot = ""
   GoTo E
Else
   PathRoot = Mid(RfPath, 1, k)
End If

If CPU <> "Mac" Then
   'username = Environ("username")    '16/5/2005
   PathRoot = Environ("userprofile") & PS '17/5/2005
   PathRoot = PathRoot  'tmp for test
   'PathRoot = PathRoot & PS  'remove 17/5/2005
Else
   'username = Environ("username")    '16/5/2005 ,Environ not available in Mac
   username = Application.username    'problem: always Tim Cole, can not identify other user in Mac
   'Message = "Enter login user name"    ' can not check a dir in Mac, e.g. use Dir(PathRoot) '13/06/2005 remove
   'username = LCase(InputBox(Message))  '13/06/2005 remove, only allow owner to retrieve saved info
   removeSP username      '16/5/2005 in Mac no space, PC keep space
   PathRoot = PathRoot & "users:" & username & ":"
End If
Exit Sub
E:
err = 1
End Sub
Sub GetScaName()
'called in frmWtgain_initialize
AgeScale(1) = "y"
AgeScale(2) = "m"
AgeScale(3) = "w"
AgeScale(4) = "d"

End Sub

Function cSDS(sexRange As Variant, tRange As Variant, DAgeU As String, Yrange As Variant, agname As String, meaName As String, Dfile As String) As Variant

Dim LL As Single, MM As Single, SS As Single, tmin As Single, tmax As Single
Dim cols As Integer, t As Single, Y As Single, AgeCol As String, MeaCol As String
Dim k As Long, ScrFail As Integer, DataAgeCol As String, DataMeaCol As String
Dim AgeR As Single, RAgeU As String, Nm As Integer   '7/3/2005
'On Error Resume Next
On Error GoTo E
cSDS = unknown

AgeCol = agname       '29/11/2004
MeaCol = meaName      '17/11/2004

If IsBookOpen(Dfile) = False Then
   If Not IsDiskFile(Dfile) Then
      Exit Function
   Else
      Workbooks.Open Dfile
   End If
End If
If IsNameExist(AgeCol, Dfile) = False Then
   Exit Function
End If
If IsNameExist(MeaCol, Dfile) = False Then
   Exit Function
End If
DataAgeCol = Dfile & "!" & AgeCol
DataMeaCol = Dfile & "!" & MeaCol

'check sex
    If IsMissing(sexRange) = True Then GoTo E
    If sexRange = "" Then GoTo E
    If (Not IsNumeric(sexRange)) Then
        If UCase(Trim(sexRange)) = "M" Or UCase(Trim(sexRange)) = "MALE" Then   '17/8/2005
           cols = 3
        Else
          If UCase(Trim(sexRange)) = "F" Or UCase(Trim(sexRange)) = "FEMALE" Then  '17/8/2005
             cols = 6
          Else
             GoTo E
          End If
        End If
    Else
       If sexRange = 1 Then
          cols = 3
       Else
          If sexRange = 2 Then
             cols = 6
          Else
             GoTo E
          End If
       End If
    End If
    'Check age
    If IsMissing(tRange) = True Then GoTo E
    If tRange = "" Then GoTo E
    If (Not IsNumeric(tRange)) Then GoTo E
    k = Range(DataAgeCol).Rows.Count
    tmin = Range(DataAgeCol).Rows(1)
    tmax = Range(DataAgeCol).Rows(k)
    'nm = InStrRev(AgeCol, "_")     '7/3/2005
    Nm = RevSearch(AgeCol, "_")    '22/3/2005
    If Nm <> 0 Then RAgeU = Mid(AgeCol, Nm + 1, Len(AgeCol) - Nm) Else GoTo E '7/3/2005
    getAgeRate DAgeU, RAgeU, AgeR   '7/3/2005
    t = tRange * AgeR   '3/2/2005
    ' tmin= -0.326 and tmax = 23 in lmsdata.xls
    If (t < tmin) Or (t > tmax) Then GoTo E
   'check yy
    If IsMissing(Yrange) Then GoTo E
    If Yrange = "" Then GoTo E
    If (Not IsNumeric(Yrange)) Then GoTo E

Y = Yrange
If Y <= 0 Then GoTo E
BinarySearch t, DataAgeCol, DataMeaCol, cols, LL, MM, SS, ScrFail
If ScrFail = 1 Then GoTo E
cSDS = zLMS(Y, LL, MM, SS)   '21/6/2007 use zLMS for calc z

'cSDS = Format(cSDS, "#0.00")   'eg 12.295 -> 12.30  13/5/2003
'If Abs(cSDS) >= Zcutoff Then GoTo E  'remove 6/3/2009
'cSDS = Round(cSDS, 3)           'eg 12.295 -> 12.3  22/5/2003 not available in Mac
'cSDS = Int(cSDS * 100 + 0.5) / 100    '10/6/2003, 31/3/2005 2 decimals, remove 29/11/2005
'-------------------------remove 9/11/2007
'Dim Ntmp As Integer
'Ntmp = 10 ^ idxDec_P
'cSDS = Int(cSDS * Ntmp + 0.5) / Ntmp   '29/11/2005
'-------------------------remove 9/11/2007
Exit Function

E:
'MsgBox "problem in cSDS", 48, "LMSgrowth"   'remove 15/9/2004
End Function
Function cSD(Fidx As Integer, sexRange As Variant, tRange As Variant, DAgeU As String, Yrange As Variant, agname As String, meaName As String, Dfile As String) As Variant
'24/7/2004 copy cSDS for six outcomes adding Sidx
Dim LL As Single, MM As Single, SS As Single, tmin As Single, tmax As Single
Dim cols As Integer, t As Single, Y As Single, AgeCol As String, MeaCol As String
Dim k As Long, ScrFail As Integer, DataAgeCol As String, DataMeaCol As String
Dim AgeR As Single, RAgeU As String, Nm As Integer   '7/3/2005
'On Error Resume Next
On Error GoTo E
cSD = unknown

AgeCol = agname       '29/11/2004
MeaCol = meaName      '17/11/2004

If IsBookOpen(Dfile) = False Then
   If Not IsDiskFile(Dfile) Then
      Exit Function
   Else
      Workbooks.Open Dfile
   End If
End If
If IsNameExist(AgeCol, Dfile) = False Then
   Exit Function
End If
If IsNameExist(MeaCol, Dfile) = False Then
   Exit Function
End If
DataAgeCol = Dfile & "!" & AgeCol
DataMeaCol = Dfile & "!" & MeaCol

'check sex
If IsMissing(sexRange) = True Then GoTo E
If sexRange = "" Then GoTo E
If (Not IsNumeric(sexRange)) Then
    If UCase(Trim(sexRange)) = "M" Or UCase(Trim(sexRange)) = "MALE" Then   '17/8/2005
        cols = 3
    Else
        If UCase(Trim(sexRange)) = "F" Or UCase(Trim(sexRange)) = "FEMALE" Then  '17/8/2005
            cols = 6
        Else
            GoTo E
        End If
    End If
Else
    If sexRange = 1 Then
        cols = 3
    Else
        If sexRange = 2 Then
            cols = 6
        Else
            GoTo E
        End If
    End If
End If

'Check age
If IsMissing(tRange) = True Then GoTo E
If tRange = "" Then GoTo E
If (Not IsNumeric(tRange)) Then GoTo E
k = Range(DataAgeCol).Rows.Count
tmin = Range(DataAgeCol).Rows(1)
tmax = Range(DataAgeCol).Rows(k)
'nm = InStrRev(AgeCol, "_")     '7/3/2005
Nm = RevSearch(AgeCol, "_")    '22/3/2005
If Nm <> 0 Then RAgeU = Mid(AgeCol, Nm + 1, Len(AgeCol) - Nm) Else GoTo E '7/3/2005
getAgeRate DAgeU, RAgeU, AgeR   '7/3/2005
t = tRange * AgeR   '3/2/2005
' tmin= -0.326 and tmax = 23 in lmsdata.xls
If (t < tmin) Or (t > tmax) Then GoTo E

'check yy   'add Fidx < 4 15/4/2011
If IsMissing(Yrange) And Fidx < 4 Then GoTo E
If Yrange = "" And Fidx < 4 Then GoTo E
If (Not IsNumeric(Yrange)) And Fidx < 4 Then GoTo E
'If IsMissing(Yrange) Then GoTo E
'If Yrange = "" Then GoTo E
'If (Not IsNumeric(Yrange)) Then GoTo E
Y = Yrange
'If Y <= 0 Then GoTo E
If Y <= 0 And Fidx < 4 Then GoTo E

BinarySearch t, DataAgeCol, DataMeaCol, cols, LL, MM, SS, ScrFail
If ScrFail = 1 Then GoTo E
'cSD = zLMS(Y, LL, MM, SS)   '21/6/2007 use zLMS for calc z
Select Case Fidx   '24/7/2007 add copy from getFNC
   Case 1  'SDS
        cSD = zLMS(Y, LL, MM, SS)
   Case 2  'centiles
        cSD = PZ(zLMS(Y, LL, MM, SS)) * 100
   Case 3  '%Predicted
        cSD = 100 * Y / MM
   Case 4  'Predicted
        cSD = MM
   Case 5  '%CV
        cSD = SS * 100
   Case 6  'Skewness
        cSD = LL
   Case 7  'lower limit notnal base on 5th centile - LLN
        cSD = LLN(LL, MM, SS)
End Select
'cSD = Format(cSD, "#0.00")   'eg 12.295 -> 12.30  13/5/2003
'If Abs(cSD) >= Zcutoff Then GoTo E
'cSD = Round(cSD, 3)           'eg 12.295 -> 12.3  22/5/2003 not available in Mac
'cSD = Int(cSD * 100 + 0.5) / 100    '10/6/2003, 31/3/2005 2 decimals, remove 29/11/2005
'-------------------------remove 9/11/2007
'Dim Ntmp As Integer
'Ntmp = 10 ^ idxDec_P
'cSD = Int(cSD * Ntmp + 0.5) / Ntmp   '29/11/2005
'-------------------------remove 9/11/2007
Exit Function

E:
'MsgBox "problem in cSD", 48, "LMSgrowth"   'remove 15/9/2004
t = t 'for test
End Function


Function cFNC(Fidx As Integer, sexRange As Variant, tRange As Variant, DAgeU As String, Yrange As Variant, agname As String, meaName As String, Dfile As String, Optional Crange1 As Variant, Optional Crange2 As Variant) As Variant
 'modify cSDS for 2 covariates  15/5/2007
Dim LL As Single, MM As Single, SS As Single, tmin As Single, tmax As Single
Dim cols As Integer, t As Single, Y As Single, AgeCol As String, MeaCol As String
Dim k As Long, ScrFail As Integer, DataAgeCol As String, DataMeaCol As String
Dim AgeR As Single, RAgeU As String, Nm As Integer   '7/3/2005
'On Error Resume Next
On Error GoTo E

cFNC = unknown    '15/9/2004 movr from bottom

AgeCol = agname       '29/11/2004
MeaCol = meaName      '17/11/2004

If IsBookOpen(Dfile) = False Then
   If Not IsDiskFile(Dfile) Then
      Exit Function
   Else
      Workbooks.Open Dfile
   End If
End If
If IsNameExist(AgeCol, Dfile) = False Then
   Exit Function
End If
If IsNameExist(MeaCol, Dfile) = False Then
   Exit Function
End If
DataAgeCol = Dfile & "!" & AgeCol
DataMeaCol = Dfile & "!" & MeaCol

'check sex
If IsMissing(sexRange) = True Then GoTo E
If sexRange = "" Then GoTo E
If (Not IsNumeric(sexRange)) Then
    'If sexRange = "M" Or sexRange = "m" Then
    If UCase(Trim(sexRange)) = "M" Or UCase(Trim(sexRange)) = "MALE" Then   '17/8/2005
       cols = 3
    Else
      'If sexRange = "F" Or sexRange = "f" Then
       If UCase(Trim(sexRange)) = "F" Or UCase(Trim(sexRange)) = "FEMALE" Then  '17/8/2005
          cols = 6
       Else
          GoTo E
       End If
    End If
Else
    If sexRange = 1 Then
       cols = 3
    Else
       If sexRange = 2 Then
          cols = 6
       Else
          GoTo E
       End If
    End If
End If

'Check age
If IsMissing(tRange) = True Then GoTo E
If tRange = "" Then GoTo E
If (Not IsNumeric(tRange)) Then GoTo E
k = Range(DataAgeCol).Rows.Count
tmin = Range(DataAgeCol).Rows(1)
tmax = Range(DataAgeCol).Rows(k)
Nm = RevSearch(AgeCol, "_")    '22/3/2005
If Nm <> 0 Then RAgeU = Mid(AgeCol, Nm + 1, Len(AgeCol) - Nm) Else GoTo E '7/3/2005
getAgeRate DAgeU, RAgeU, AgeR   '7/3/2005
t = tRange * AgeR   '3/2/2005
' tmin= -0.326 and tmax = 23 in lmsdata.xls
If (t < tmin) Or (t > tmax) Then GoTo E

''check yy ----  'move to after check Fidx 03/05/2011
'If IsMissing(Yrange) Then GoTo E
'If Yrange = "" Then GoTo E
'If (Not IsNumeric(Yrange)) Then GoTo E
'-----

'check covariate of lung function 3/4/2007,15/5/2007,22/5/2007, 21/6/2007
If IsMissing(Fidx) Then GoTo E
Dim Rt As Long, Cl As Integer, err As Integer, cov1 As Single, cov2 As Single
Rt = Range(DataAgeCol).Row
Cl = Range(DataMeaCol).Column + cols - 3

Select Case Rt   'need for refresh existing results,
   Case 10
       CovChk Dfile, Rt - 3, Cl, Crange1, cov1, err
       If err = 1 Then GoTo E
   Case 12
       CovChk Dfile, Rt - 4, Cl, Crange1, cov1, err
       If err = 1 Then GoTo E
       CovChk Dfile, Rt - 3, Cl, Crange2, cov2, err
       If err = 1 Then GoTo E
End Select

'check yy
If IsMissing(Yrange) And Fidx < 4 Then GoTo E    'add Fidx < 4 15/4/2011
If Yrange = "" And Fidx < 4 Then GoTo E          'add Fidx < 4 15/4/2011
If (Not IsNumeric(Yrange)) And Fidx < 4 Then GoTo E     'add Fidx < 4 15/4/2011
'If IsMissing(Yrange) Then GoTo E
'If Yrange = "" Then GoTo E
'If (Not IsNumeric(Yrange)) Then GoTo E
Y = Yrange
'If Y <= 0 Then GoTo E
If Y <= 0 And Fidx < 4 Then GoTo E    'add Fidx < 4 15/4/2011

BinarySearch t, DataAgeCol, DataMeaCol, cols, LL, MM, SS, ScrFail
If ScrFail = 1 Then GoTo E

'add for covariate of lung function 3/4/2007, 11/6/2007
'------
CovAdd Dfile, Rt, Cl, t, cov1, cov2, LL
CovAdd Dfile, Rt, Cl + 1, t, cov1, cov2, MM
CovAdd Dfile, Rt, Cl + 2, t, cov1, cov2, SS

'add for Lung finction 6 types of output 21/6/2007, 18/3/2011 6->7 add LLN
Select Case Fidx
   Case 1  'SDS
        cFNC = zLMS(Y, LL, MM, SS)   '21/6/2007 move codes to zLMS
   Case 2  'centiles
        cFNC = PZ(zLMS(Y, LL, MM, SS)) * 100
   Case 3  '%Predicted
        cFNC = 100 * Y / MM
   Case 4  'Predicted
        cFNC = MM
   Case 5  '%CV
        cFNC = SS * 100
   Case 6  'Skewness
        cFNC = LL
   Case 7  'lower limit normal - LLN based on 5th centile 18/3/2011
        cFNC = LLN(LL, MM, SS)
End Select
'-----
'If Abs(cFNC) >= Zcutoff Then GoTo E   'remove 22/6/2007
'cFNC = Format(cFNC, "#0.00")   'eg 12.295 -> 12.30  13/5/2003
'cFNC = Round(cFNC, 3)          'eg 12.295 -> 12.3  22/5/2003 not available in Mac
'-------------------------remove 9/11/2007
'Dim Ntmp As Integer
'Ntmp = 10 ^ idxDec_P    '29/11/2005 user determined, default 2
'cFNC = Int(cFNC * Ntmp + 0.5) / Ntmp
'-------------------------remove 9/11/2007

Exit Function

E:
'MsgBox "problem in cFNC", 48, "LMSgrowth"   'remove 15/9/2004
cFNC = cFNC
End Function








Sub IOTFYMWD(iSex As Integer, idxB As Integer)
'2/7/2003 for IOTF, mixed sex
Dim j1 As Integer, j2 As Integer, j3 As Integer, cur As String, DaRow1_I_adj As Long    '28/1/2005
Dim tmpDAgeU As String   '8/3/2005
On Error GoTo E
cur = ColName(idxM2_I)   'use 256 columns
If NHead_I = 1 Then  '28/1/2005  add *_adj
   DaRow1_I_adj = DaRow1_I + 1
   Range(cur & DaRow1_I).value = "IOTFgrade"   '4/3/2005
Else
   DaRow1_I_adj = DaRow1_I
End If
If DaRow1_I_adj > DaRow2_I Then Exit Sub
j1 = idxSex_I - 1 - idxM2_I
j2 = idxAge_I - idxM2_I
'j3 = idxM1_I - idxM2_I    'remove 15/8/2005
j3 = idxB - idxM2_I    '15/8/2005 idxB = idxWH_I if use Wt & Ht, = idxM1_I if use BMI
Range(cur & DaRow1_I_adj).Select    '28/1/2005
tmpDAgeU = Chr(34) & frmIOTFCo!lblAgeU.Caption & Chr(34)       '8/3/2005
Dim Ssex As Variant  '4/3/2005
Select Case iSex     '4/3/2005
   Case 0
        Ssex = Chr(34) & "M" & Chr(34)
   Case 1
        Ssex = Chr(34) & "F" & Chr(34)
   Case Is > 1
        Ssex = "RC[" & j1 & "]"
End Select
ActiveCell.FormulaR1C1 = "=cIOTF2(" & Ssex & ",RC[" & j2 & "]," & tmpDAgeU & ",RC[" & j3 & "])"   '23/4/2007
'ActiveCell.FormulaR1C1 = "=cIOTF(" & Ssex & ",RC[" & j2 & "]," & tmpDAgeU & ",RC[" & j3 & "])"   '23/11/2004
If DaRow2_I > DaRow1_I_adj Then    '28/1/2005
   Range(cur & DaRow1_I_adj).Select
   Selection.AutoFill Destination:=Range(cur & DaRow1_I_adj & ":" & cur & DaRow2_I), Type:=xlFillDefault
End If
Exit Sub
E:
'MsgBox "Error in IOTFYMWD", 48, "LMSgrowth"   'remove 10/9/2004
End Sub



Sub ListFiles()
'28/03/2003
Dim k As Integer, f, s
ReDim RfFiles(100)
's = RfPath & "\"  'remove 4/6/2003
s = RfPath & PS    '4/6/2003
k = 1
'first file
f = Dir(s, 0)
RfFiles(k) = f
'get remaining files
Do While f <> ""
   f = Dir
   If f <> "" Then
      k = k + 1
      RfFiles(k) = f
   End If
Loop
RfTotal = k
End Sub

Function cSDSGAIN(Age1 As Variant, Scale1 As Variant, Wtsds1 As Variant, Age2 As Variant, Scale2 As Variant, Wtsds2 As Variant) As Variant
'keep old function of Tim !!!!! 8/3/2005
Dim t1 As Single, t2 As Single, sd1 As Single, sd2 As Single, adj1 As Single, adj2 As Single
Dim s1 As String, s2 As String, gapwk As Single, meanwk As Single, lngapwk As Single, lnmeanwk As Single, wk As Single
Dim FisherZ As Single, exp2z As Single, r As Single
Dim B1 As Single, B2 As Single, B3 As Single, B4 As Single, B5 As Single, B6 As Single  '29/5/2003
'On Error Resume Next
On Error GoTo E

cSDSGAIN = unknown
'Application.ScreenUpdating = False  'remove 21/9/2004

'check age1
If IsMissing(Age1) = True Then GoTo E
If Age1 = "" Then GoTo E
If (Not IsNumeric(Age1)) Then GoTo E

'check age2
If IsMissing(Age2) = True Then GoTo E
If Age2 = "" Then GoTo E
If (Not IsNumeric(Age2)) Then GoTo E

'Check scale1
If IsMissing(Scale1) = True Then
   s1 = "X"
Else
   If Scale1 = "" Then
      s1 = "X"
   Else
      s1 = Scale1
      s1 = Left(Trim(s1), 1)
   End If
End If
'Check scale2
If IsMissing(Scale2) = True Then
   s2 = "X"
Else
   If Scale2 = "" Then
      s2 = "X"
   Else
      s2 = Scale2
      s2 = Left(Trim(s2), 1)
   End If
End If

'check wtds1
If IsMissing(Wtsds1) = True Then GoTo E
If Wtsds1 = unknown Then GoTo E
If (Not IsNumeric(Wtsds1)) Then GoTo E
'check wtds2
If IsMissing(Wtsds2) = True Then GoTo E
If Wtsds2 = unknown Then GoTo E
If (Not IsNumeric(Wtsds2)) Then GoTo E
If Abs(Wtsds1) >= 8 Or Abs(Wtsds2) >= 8 Then GoTo E
wk = 365.25 / 7
Select Case s1
    Case "Y", "y"
        adj1 = 1
    Case "M", "m"
        adj1 = 12
    Case "W", "w"
        adj1 = wk    '365.25 / 7
    Case "D", "d"
        adj1 = 365.25
    Case "X"
        adj1 = -99    'allow one missing
    Case Else
        adj1 = -99
End Select
Select Case s2
    Case "Y", "y"
        adj2 = 1
    Case "M", "m"
        adj2 = 12
    Case "W", "w"
        adj2 = wk     '365.25 / 7
    Case "D", "d"
        adj2 = 365.25
    Case "X"
        adj2 = -99    'allow one missing
    Case Else
        adj2 = -99
End Select
If adj1 = -99 And adj2 = -99 Then
   adj1 = 1: adj2 = 1
Else
   If adj1 = -99 And adj2 <> -99 Then adj1 = adj2
   If adj1 <> -99 And adj2 = -99 Then adj2 = adj1
End If
t1 = Age1 / adj1: t2 = Age2 / adj2   'in year
'If t1 < 0 Or t2 < 0 Or t1 > 2 Or t2 > 2 Then  '27/3/2002  Tim 1998 ref remove 12/8/2005
If t1 < -0.00001 Or t2 < -0.00001 Or t1 > 2.00001 Or t2 > 2.00001 Then  'add 0.00001 to adjust round differences in single and integer
      'MsgBox ("Age < 0 wk or > 2yr")
      GoTo E
End If
gapwk = (t2 - t1) * wk
'If gapwk < 4 Then       'gapwk (single) and may slightly diff to 4 even it is 4 11/8/2005
If gapwk < 3.99999 Then
      'MsgBox ("Age  gap < 4 wk")
      GoTo E
End If
meanwk = (t1 + t2) / 2 * wk
lngapwk = Log(gapwk)
lnmeanwk = Log(meanwk)
B1 = 3.1775     'constant, 1995 was 3.16 now use 1998's results
B2 = -1.4811    'coefficient of lngapwk, was -1.56
B3 = 0.1991     'coefficient of lnmeanwk*lngapwk of age, was 0.225
B4 = -2.029     'coefficient of 1/lngapwk, was -2.04
B5 = 0.3256     'coefficient of lnmeanwk, was 0.384
B6 = -0.04601       '-0.0643
FisherZ = B1 + B2 * lngapwk + B3 * lnmeanwk * lngapwk + B4 / gapwk + lnmeanwk * (B5 + lnmeanwk * B6) 'Z, Fisher's transform
exp2z = Exp(2 * FisherZ)
r = (exp2z - 1) / (exp2z + 1)
cSDSGAIN = (Wtsds2 - r * Wtsds1) / ((1 - r * r) ^ (1 / 2))
'cSDSGAIN = Round(cSDSGAIN, 3)  '22/5/2003 Round function not available in Mac
'cSDSGAIN = Int(cSDSGAIN * 100 + 0.5) / 100 '10/6/2003, remove 29/11/2005
'-------------------------remove 9/11/2007
'Dim Ntmp As Integer
'Ntmp = 10 ^ idxDec_P
'cSDSGAIN = Int(cSDSGAIN * Ntmp + 0.5) / Ntmp   '29/11/2005
'-------------------------remove 9/11/2007
'Application.ScreenUpdating = True  'remove 21/9/2004
Exit Function

E:
'MsgBox "problem in cSDSGAIN", 48, "LMSgrowth"   'remove 15/9/2004
'Application.ScreenUpdating = True   'remove 21/9/2004
End Function
Function SDSGAIN(Age1 As Variant, Scale1 As Variant, Wtsds1 As Variant, Age2 As Variant, Scale2 As Variant, Wtsds2 As Variant) As Variant
'keep old function of Tim !!!!! 8/3/2005
Dim t1 As Single, t2 As Single, sd1 As Single, sd2 As Single, adj1 As Single, adj2 As Single
Dim s1 As String, s2 As String, gapwk As Single, meanwk As Single, lngapwk As Single, lnmeanwk As Single, wk As Single
Dim FisherZ As Single, exp2z As Single, r As Single
Dim B1 As Single, B2 As Single, B3 As Single, B4 As Single, B5 As Single, B6 As Single  '29/5/2003
'On Error Resume Next
On Error GoTo E

SDSGAIN = unknown   '15/9/2004 move from bottom
'Application.ScreenUpdating = False  'remove 21/9/2004

'check age1
If IsMissing(Age1) = True Then GoTo E
If Age1 = "" Then GoTo E
If (Not IsNumeric(Age1)) Then GoTo E

'check age2
If IsMissing(Age2) = True Then GoTo E
If Age2 = "" Then GoTo E
If (Not IsNumeric(Age2)) Then GoTo E

'Check scale1
If IsMissing(Scale1) = True Then
   s1 = "X"
Else
   If Scale1 = "" Then
      s1 = "X"
   Else
      s1 = Scale1
      s1 = Left(Trim(s1), 1)
   End If
End If
'Check scale2
If IsMissing(Scale2) = True Then
   s2 = "X"
Else
   If Scale2 = "" Then
      s2 = "X"
   Else
      s2 = Scale2
      s2 = Left(Trim(s2), 1)
   End If
End If

'check wtds1
If IsMissing(Wtsds1) = True Then GoTo E
If Wtsds1 = unknown Then GoTo E
If (Not IsNumeric(Wtsds1)) Then GoTo E

'check wtds2
If IsMissing(Wtsds2) = True Then GoTo E
If Wtsds2 = unknown Then GoTo E
If (Not IsNumeric(Wtsds2)) Then GoTo E

If Abs(Wtsds1) >= 8 Or Abs(Wtsds2) >= 8 Then GoTo E
wk = 365.25 / 7
Select Case s1
    Case "Y", "y"
        adj1 = 1
    Case "M", "m"
        adj1 = 12
    Case "W", "w"
        adj1 = wk    '365.25 / 7
    Case "D", "d"
        adj1 = 365.25
    Case "X"
        adj1 = -99
    Case Else
        adj1 = -99
End Select
Select Case s2
    Case "Y", "y"
        adj2 = 1
    Case "M", "m"
        adj2 = 12
    Case "W", "w"
        adj2 = wk     '365.25 / 7
    Case "D", "d"
        adj2 = 365.25
    Case "X"
        adj2 = -99
    Case Else
        adj2 = -99
End Select
If adj1 = -99 And adj2 = -99 Then
   adj1 = 1: adj2 = 1
Else
   If adj1 = -99 And adj2 <> -99 Then adj1 = adj2
   If adj1 <> -99 And adj2 = -99 Then adj2 = adj1
End If
t1 = Age1 / adj1: t2 = Age2 / adj2   'in year
'If t1 < -0.0767 Or t2 < 0.0767 Or t1 > 2 Or t2 > 2 Then  '27/3/2002 remove
If t1 < 0 Or t2 < 0 Or t1 > 2 Or t2 > 2 Then  '27/3/2002  Tim 1998 ref
      'MsgBox ("Age < 0 wk or > 2yr")
      GoTo E
End If
gapwk = (t2 - t1) * wk
If gapwk < 4 Then
      'MsgBox ("Age  gap < 4 wk")
      GoTo E
End If
meanwk = (t1 + t2) / 2 * wk
lngapwk = Log(gapwk)
lnmeanwk = Log(meanwk)
B1 = 3.1775     'constant, 1995 was 3.16 now use 1998's results
B2 = -1.4811    'coefficient of lngapwk, was -1.56
B3 = 0.1991     'coefficient of lnmeanwk*lngapwk of age, was 0.225
B4 = -2.029     'coefficient of 1/lngapwk, was -2.04
B5 = 0.3256     'coefficient of lnmeanwk, was 0.384
B6 = -0.04601       '-0.0643
FisherZ = B1 + B2 * lngapwk + B3 * lnmeanwk * lngapwk + B4 / gapwk + lnmeanwk * (B5 + lnmeanwk * B6) 'Z, Fisher's transform
exp2z = Exp(2 * FisherZ)
r = (exp2z - 1) / (exp2z + 1)
SDSGAIN = (Wtsds2 - r * Wtsds1) / ((1 - r * r) ^ (1 / 2))
'SDSGAIN = Round(SDSGAIN, 3)  '22/5/2003 Round function not available in Mac
SDSGAIN = Int(SDSGAIN * 1000 + 0.5) / 1000 '10/6/2003

'Application.ScreenUpdating = True  'remove 21/9/2004
Exit Function

E:
'MsgBox "problem in SDSGAIN", 48, "LMSgrowth"   'remove 15/9/2004
'Application.ScreenUpdating = True   'remove 21/9/2004
End Function

Sub OpenIOTF()

Dim err As Integer
'err = 0
Application.ScreenUpdating = False
On Error GoTo E
CPU = Application.OperatingSystem    '4/6/2003 move from Auto_open
PS = Application.PathSeparator
If CPU = "Mac" Then ZoomSize = ZoomMac Else ZoomSize = ZoomPC
If NOpenRf < 1 Then  '30/10/2003
   getExistingXY err
   If err = 1 Then GoTo E
   ZPInit     '16/5/2005
   ZPopen     '16/5/2005
   NOpenRf = NOpenRf + 1
End If
getIOTFRf
getIOTFm    '23/4/2007
getIOTFf    '23/4/2007 to add thinness, keep getIOTFRf for old results re-frash
frmIOTFCo.Show
Application.ScreenUpdating = True
Exit Sub

E:
'MsgBox ("error in OpenIOTF"), 48, "LMSgrowth"
Application.ScreenUpdating = True
End Sub

Sub OpenSelectRf()
'27/03/2003
Dim err As Integer
Application.ScreenUpdating = False
On Error GoTo E
'err = 0
CPU = Application.OperatingSystem    '4/6/2003 move from Auto_open
PS = Application.PathSeparator
If CPU = "Mac" Then ZoomSize = ZoomMac Else ZoomSize = ZoomPC
If NOpenRf < 1 Then
   getExistingXY err     '20/6/2003 call getPathRoot
   If err = 1 Then GoTo E
   ZPInit     '16/5/2005
   ZPopen     '16/5/2005
   NOpenRf = NOpenRf + 1   '15/5/2003
End If
ListFiles   'get RfFiles(), RfTotal  from RfPath of ..\XLSTART\
frmSelectRf.Show
Application.ScreenUpdating = True
Exit Sub

E:
Application.ScreenUpdating = True

End Sub

Function PZ(x As Single) As Double

On Error GoTo E
'note calc x of sds to PZ of p

' This file includes the Applied Statistics algorithm AS 66 for calculating
' the tail area under the normal curve, and two alternative routines which
' give higher accuracy.   The latter have been contributed by Alan Miller of
' CSIRO Division of Mathematics & Statistics, Clayton, Victoria.   Notice
' that each function or routine has different call arguments.
'
' Algorithm AS66 Applied Statistics (1973) vol22 no.3
'
' Evaluates the tail area of the standardised normal curve
' from x to infinity if upper is .true. or
' from minus infinity to x if upper is .false.

Dim zero As Double, one As Double, half As Double
Dim con As Double, z As Double, Y As Double
Dim p As Double, q As Double, r As Double, a1 As Double, a2 As Double, a3 As Double
Dim B1 As Double, B2 As Double, c1 As Double, c2 As Double, c3 As Double, c4 As Double, c5 As Double, c6 As Double
Dim d1 As Double, d2 As Double, d3 As Double, d4 As Double, d5 As Double
Dim upper As Boolean, up As Boolean 'True = -1, false = 0
Dim ltone As Double, utzero As Double

zero = 0#: one = 1#: half = 0.5
ltone = 7#: utzero = 18.66: con = 1.28
p = 0.398942280444: q = 0.39990348504: r = 0.398942280385
a1 = 5.75885480458: a2 = 2.62433121679: a3 = 5.92885724438
B1 = -29.8213557807: B2 = 48.6959930692
c1 = -3.8052 / 100000000: c2 = 3.98064794 / 10000: c3 = -0.151679116635
c4 = 4.8385912808: c5 = 0.742380924027: c6 = 3.99019417011
d1 = 1.00000615302: d2 = 1.98615381364: d3 = 5.29330324926
d4 = -15.1508972451: d5 = 30.789933034
      
upper = False
up = upper
z = x
If (z >= zero) Then GoTo G10
    up = Not up
    z = -z
G10:
If (z <= ltone Or up And z <= utzero) Then GoTo G20
    PZ = zero
    GoTo G40
G20:
Y = half * z * z
If (z > con) Then GoTo G30
'note I meet problem to use multiple of dividend, so separate
PZ = Y + a2 + B2 / (Y + a3)
PZ = Y + a1 + B1 / PZ
PZ = half - z * (p - q * Y / PZ)
'PZ = half - z * (p - q * y / (y + a1 + b1 / (y + a2 + b2 / (y + a3))))  'error, why?
GoTo G40
G30:
PZ = z + c5 + d5 / (z + c6)
PZ = z + c4 + d4 / PZ
PZ = z + c3 + d3 / PZ
PZ = z + c2 + d2 / PZ
PZ = z + c1 + d1 / PZ
PZ = r * Exp(-Y) / PZ
'PZ = r * Exp(-y) / (z + c1 + d1 / (z + c2 + d2 / (z + c3 + d3 / (z + c4 + d4 / (z + c5 + d5 / (z + c6)))))) 'can not run, error, why?
G40:
If (Not up) Then PZ = one - PZ
PZ = PZ
Exit Function
E:
'MsgBox ("Problem in PZ"), 48, "LMSgrowth"  'remove 15/9/2004
End Function
Sub BinarySearch(Schfor As Single, tcol As String, ycol As String, cols As Integer, LL As Single, MM As Single, SS As Single, ScrFail As Integer)
Dim i As Long, Hi As Long, Lo As Long, Median As Long
Dim idx1 As Long, idx2 As Long, idx3 As Long, idx0 As Long, Hi_o As Long, Lo_o As Long

On Error GoTo E

ScrFail = 1  '1-search failure
idx1 = 0
idx2 = 0
Schfor = CSng(Schfor)

'my BinarySearch
Hi_o = Range(ycol).Rows.Count    '28/2/2005   see sub ChkZPRows in frmZP for alternative method for Lo
For i = 1 To Hi_o   '28/2/2005
    If Range(ycol).Cells(i, cols - 1) <> 0 Then GoTo nmnm
Next i
nmnm:
Lo_o = i
If Lo_o = Hi_o Then Exit Sub  '28/2/2005

'14/12/2010 check the blanks at bottom range of the name
For i = Lo_o To Hi_o   '14/12/2010
    'If Range(ycol).Cells(i, cols - 1) = 0 Then GoTo mnmn
    If Range(ycol).Cells(i, cols - 1) = 0 And Range(ycol).Cells(i + 1, cols - 1) = 0 Then GoTo mnmn '19/1/2011 allow one row missing in the mid of name
Next i
mnmn:
Hi_o = i - 1   'end of 14/12/2010 added

Lo = Lo_o: Hi = Hi_o
Do
  Median = (Lo + Hi) \ 2 'integer division
  If Schfor = Range(tcol).Rows(Median) Then
     ScrFail = 0
     idx1 = Median
     idx2 = Median
     Exit Do
  End If
  If (Schfor < Range(tcol).Rows(Median)) Then
      If Median = Lo Then
         Exit Do
      Else
         If Schfor > Range(tcol).Rows(Median - 1) Then
            ScrFail = 0
            idx1 = Median - 1
            idx2 = Median
            Exit Do
         Else
            If Schfor = Range(tcol).Rows(Median - 1) Then
               ScrFail = 0
               idx1 = Median - 1
               idx2 = Median - 1
               Exit Do
            Else
               Hi = Median - 1
            End If
         End If
      End If
  Else
     If Median = Hi Then
        Exit Do
     Else
        If Schfor < Range(tcol).Rows(Median + 1) Then
           ScrFail = 0
           idx1 = Median
           idx2 = Median + 1
           Exit Do
        Else
           If Schfor = Range(tcol).Rows(Median + 1) Then
              ScrFail = 0
              idx1 = Median + 1
              idx2 = Median + 1
              Exit Do
           Else
              Lo = Median + 1
           End If
        End If
     End If
  End If
Loop Until (Lo > Hi)
If ScrFail = 1 Then Exit Sub
'-------------

If Range(ycol).Cells(idx1, cols - 1) = 0 Or Range(ycol).Cells(idx2, cols - 1) = 0 Then
   ScrFail = 1
   Exit Sub
End If
If idx1 <> idx2 Then  'modified 28/2/2005
   If idx1 = Lo_o Or idx2 = Hi_o Then   '28/2/2005
      LL = interpL(Schfor, Range(tcol).Rows(idx1), Range(tcol).Rows(idx2), Range(ycol).Cells(idx1, cols - 2), Range(ycol).Cells(idx2, cols - 2))
      MM = interpL(Schfor, Range(tcol).Rows(idx1), Range(tcol).Rows(idx2), Range(ycol).Cells(idx1, cols - 1), Range(ycol).Cells(idx2, cols - 1))
      SS = interpL(Schfor, Range(tcol).Rows(idx1), Range(tcol).Rows(idx2), Range(ycol).Cells(idx1, cols), Range(ycol).Cells(idx2, cols))
   Else
      If Range(ycol).Cells(idx1, cols - 1) = 0 Then idx1 = idx1 - 1    '19/1/2011 for allowing missing vlaues at 3y in USCDC2000
      If Range(ycol).Cells(idx2, cols - 1) = 0 Then idx2 = idx2 + 1    '19/1/2011 for allowing missing vlaues at 3y in USCDC2000
      idx3 = idx2 + 1
      idx0 = idx1 - 1     '29/2/2008
      If Range(ycol).Cells(idx0, cols - 1) = 0 Then idx0 = idx0 - 1    '19/1/2011 for allowing missing vlaues at 3y in USCDC2000
      If Range(ycol).Cells(idx3, cols - 1) = 0 Then idx3 = idx3 + 1    '19/1/2011 for allowing missing vlaues at 3y in USCDC2000
      If (Range(tcol).Rows(idx0) = Range(tcol).Rows(idx1) And Range(ycol).Cells(idx0, cols - 1) <> Range(ycol).Cells(idx1, cols - 1)) Or (Range(tcol).Rows(idx2) = Range(tcol).Rows(idx3) And Range(ycol).Cells(idx2, cols - 1) <> Range(ycol).Cells(idx3, cols - 1)) Then  '11/6/2008
         LL = interpL(Schfor, Range(tcol).Rows(idx1), Range(tcol).Rows(idx2), Range(ycol).Cells(idx1, cols - 2), Range(ycol).Cells(idx2, cols - 2))
         MM = interpL(Schfor, Range(tcol).Rows(idx1), Range(tcol).Rows(idx2), Range(ycol).Cells(idx1, cols - 1), Range(ycol).Cells(idx2, cols - 1))
         SS = interpL(Schfor, Range(tcol).Rows(idx1), Range(tcol).Rows(idx2), Range(ycol).Cells(idx1, cols), Range(ycol).Cells(idx2, cols))
      Else
        If Range(tcol).Rows(idx0) = Range(tcol).Rows(idx1) And Range(ycol).Cells(idx1, cols - 1) = Range(ycol).Cells(idx0, cols - 1) Then  '11/6/2008
           idx0 = idx0 - 1
        End If
        If Range(tcol).Rows(idx2) = Range(tcol).Rows(idx3) And Range(ycol).Cells(idx2, cols - 1) = Range(ycol).Cells(idx3, cols - 1) Then  '11/6/2008
           idx3 = idx3 + 1
        End If
        LL = interpC(Schfor, Range(tcol).Rows(idx0), Range(tcol).Rows(idx1), Range(tcol).Rows(idx2), Range(tcol).Rows(idx3), Range(ycol).Cells(idx0, cols - 2), Range(ycol).Cells(idx1, cols - 2), Range(ycol).Cells(idx2, cols - 2), Range(ycol).Cells(idx3, cols - 2))   '29/2/2008 include idx0
        MM = interpC(Schfor, Range(tcol).Rows(idx0), Range(tcol).Rows(idx1), Range(tcol).Rows(idx2), Range(tcol).Rows(idx3), Range(ycol).Cells(idx0, cols - 1), Range(ycol).Cells(idx1, cols - 1), Range(ycol).Cells(idx2, cols - 1), Range(ycol).Cells(idx3, cols - 1))
        SS = interpC(Schfor, Range(tcol).Rows(idx0), Range(tcol).Rows(idx1), Range(tcol).Rows(idx2), Range(tcol).Rows(idx3), Range(ycol).Cells(idx0, cols), Range(ycol).Cells(idx1, cols), Range(ycol).Cells(idx2, cols), Range(ycol).Cells(idx3, cols))
        'LL = interpQ(Schfor, Range(tcol).Rows(idx1), Range(tcol).Rows(idx2), Range(tcol).Rows(idx3), Range(ycol).Cells(idx1, cols - 2), Range(ycol).Cells(idx2, cols - 2), Range(ycol).Cells(idx3, cols - 2))
        'MM = interpQ(Schfor, Range(tcol).Rows(idx1), Range(tcol).Rows(idx2), Range(tcol).Rows(idx3), Range(ycol).Cells(idx1, cols - 1), Range(ycol).Cells(idx2, cols - 1), Range(ycol).Cells(idx3, cols - 1))
        'SS = interpQ(Schfor, Range(tcol).Rows(idx1), Range(tcol).Rows(idx2), Range(tcol).Rows(idx3), Range(ycol).Cells(idx1, cols), Range(ycol).Cells(idx2, cols), Range(ycol).Cells(idx3, cols))
      End If
   End If
Else
   LL = Range(ycol).Cells(idx1, cols - 2)
   MM = Range(ycol).Cells(idx1, cols - 1)
   SS = Range(ycol).Cells(idx1, cols)
End If
'Exit Sub
E:
'MsgBox ("problem in BinarySearch"), 48, "LMSgrowth"  '10/9/2004 remove
End Sub


Sub MergeCellRC(r As Integer, c1 As Integer, c2 As Integer, Tit As String)

Range(Cells(r, c1), Cells(r, c2)).Select
    With Selection
        .HorizontalAlignment = xlCenter
        .VerticalAlignment = xlBottom
        .WrapText = False
        .Orientation = 0
        .AddIndent = False
        .ShrinkToFit = False
        .MergeCells = False
    End With
    Selection.Merge
    Range(Cells(r, c1), Cells(r, c2)).Select
    ActiveCell.FormulaR1C1 = Tit
End Sub

Sub BinarySearchI(Schfor As Single, cols As Integer, OW As Single, OB As Single, ScrFail As Integer)
'2/7/2003 for IOTF interpolation, 29/2/2008 & 11/6/2008 modify
Dim i As Long, Hi As Long, Lo As Long, Median As Long
Dim idx1 As Long, idx2 As Long, idx3 As Long, idx0 As Long
Dim Hi_o As Long, Lo_o As Long  '28/2/2005
On Error GoTo E
'9/1/2002
ScrFail = 1  '1-search failure
idx1 = 0
idx2 = 0
Schfor = CSng(Schfor)
'-----------------
'my BinartSearch
Lo_o = 1: Hi_o = 33   '28/2/2005 for the start and end of IOTF
Lo = 1: Hi = 33
Do
  Median = (Lo + Hi) \ 2 'integer division
  If Schfor = IOTFRf(Median, 0) Then
     ScrFail = 0
     idx1 = Median
     idx2 = Median
     Exit Do
  End If
  If Schfor < IOTFRf(Median, 0) Then
      If Median = Lo Then
         Exit Do
      Else
         If Schfor > IOTFRf(Median - 1, 0) Then
            ScrFail = 0
            idx1 = Median - 1
            idx2 = Median
            Exit Do
         Else
            If Schfor = IOTFRf(Median - 1, 0) Then
               ScrFail = 0
               idx1 = Median - 1
               idx2 = Median - 1
               Exit Do
            Else
               Hi = Median - 1
            End If
         End If
      End If
  Else
     If Median = Hi Then
        Exit Do
     Else
        If Schfor < IOTFRf(Median + 1, 0) Then
           ScrFail = 0
           idx1 = Median
           idx2 = Median + 1
           Exit Do
        Else
           If Schfor = IOTFRf(Median + 1, 0) Then
              ScrFail = 0
              idx1 = Median + 1
              idx2 = Median + 1
              Exit Do
           Else
              Lo = Median + 1
           End If
        End If
     End If
  End If
Loop Until (Lo > Hi)
If ScrFail = 1 Then Exit Sub

If idx1 <> idx2 Then  '28/2/2005
   If idx1 = Lo_o Or idx2 = Hi_o Then   '28/2/2005
      OW = interpL(Schfor, IOTFRf(idx1, 0), IOTFRf(idx2, 0), IOTFRf(idx1, cols - 1), IOTFRf(idx2, cols - 1))
      OB = interpL(Schfor, IOTFRf(idx1, 0), IOTFRf(idx2, 0), IOTFRf(idx1, cols), IOTFRf(idx2, cols))
   Else
      idx3 = idx2 + 1
      idx0 = idx1 - 1     '29/2/2008
      'OW = interpQ(Schfor, IOTFRf(idx1, 0), IOTFRf(idx2, 0), IOTFRf(idx3, 0), IOTFRf(idx1, cols - 1), IOTFRf(idx2, cols - 1), IOTFRf(idx3, cols - 1))
      'OB = interpQ(Schfor, IOTFRf(idx1, 0), IOTFRf(idx2, 0), IOTFRf(idx3, 0), IOTFRf(idx1, cols), IOTFRf(idx2, cols), IOTFRf(idx3, cols))
      OW = interpC(Schfor, IOTFRf(idx0, 0), IOTFRf(idx1, 0), IOTFRf(idx2, 0), IOTFRf(idx3, 0), IOTFRf(idx0, cols - 1), IOTFRf(idx1, cols - 1), IOTFRf(idx2, cols - 1), IOTFRf(idx3, cols - 1))    '29/2/2008 include idx0
      OB = interpC(Schfor, IOTFRf(idx0, 0), IOTFRf(idx1, 0), IOTFRf(idx2, 0), IOTFRf(idx3, 0), IOTFRf(idx0, cols), IOTFRf(idx1, cols), IOTFRf(idx2, cols), IOTFRf(idx3, cols))                    '29/2/2008 include idx0
   End If
Else
   OW = IOTFRf(idx1, cols - 1)
   OB = IOTFRf(idx1, cols)
End If

Exit Sub
E:
'MsgBox ("problem in BinarySearchI"), 48, "LMSgrowth"  '10/9/2004 remove
End Sub
Sub BinarySearch2(Schfor As Single, Nsex As Integer, IOTF() As Single, cutoff() As Single, ScrFail As Integer)
'23/4/2007 IOTF interpolation for thinness & obese, modified from BinarySearchI, keep BinarySearchI for old results fresh
Dim i As Long, Hi As Long, Lo As Long, Median As Long
Dim idx1 As Long, idx2 As Long, idx3 As Long, idx0 As Long
Dim Hi_o As Long, Lo_o As Long  '28/2/2005
On Error GoTo E

ScrFail = 1  '1-search failure
idx1 = 0
idx2 = 0
Schfor = CSng(Schfor)
'-----------------
'my BinartSearch
Lo_o = 1: Hi_o = 33   '28/2/2005 for the start and end of IOTF
Lo = 1: Hi = 33
Do
  Median = (Lo + Hi) \ 2 'integer division
  If Schfor = IOTF(Median, 0) Then
     ScrFail = 0
     idx1 = Median
     idx2 = Median
     Exit Do
  End If
  If Schfor < IOTF(Median, 0) Then
      If Median = Lo Then
         Exit Do
      Else
         If Schfor > IOTF(Median - 1, 0) Then
            ScrFail = 0
            idx1 = Median - 1
            idx2 = Median
            Exit Do
         Else
            If Schfor = IOTF(Median - 1, 0) Then
               ScrFail = 0
               idx1 = Median - 1
               idx2 = Median - 1
               Exit Do
            Else
               Hi = Median - 1
            End If
         End If
      End If
  Else
     If Median = Hi Then
        Exit Do
     Else
        If Schfor < IOTF(Median + 1, 0) Then
           ScrFail = 0
           idx1 = Median
           idx2 = Median + 1
           Exit Do
        Else
           If Schfor = IOTF(Median + 1, 0) Then
              ScrFail = 0
              idx1 = Median + 1
              idx2 = Median + 1
              Exit Do
           Else
              Lo = Median + 1
           End If
        End If
     End If
  End If
Loop Until (Lo > Hi)
If ScrFail = 1 Then Exit Sub
'-------------
If idx1 <> idx2 Then  'remove 28/2/2005
   If idx1 = Lo_o Or idx2 = Hi_o Then   '28/2/2005
      cutoff(1) = interpL(Schfor, IOTF(idx1, 0), IOTF(idx2, 0), IOTF(idx1, 1), IOTF(idx2, 1))
      cutoff(2) = interpL(Schfor, IOTF(idx1, 0), IOTF(idx2, 0), IOTF(idx1, 2), IOTF(idx2, 2))
      cutoff(3) = interpL(Schfor, IOTF(idx1, 0), IOTF(idx2, 0), IOTF(idx1, 3), IOTF(idx2, 3))
      cutoff(4) = interpL(Schfor, IOTF(idx1, 0), IOTF(idx2, 0), IOTF(idx1, 4), IOTF(idx2, 4))
      cutoff(5) = interpL(Schfor, IOTF(idx1, 0), IOTF(idx2, 0), IOTF(idx1, 5), IOTF(idx2, 5))
   Else
      idx3 = idx2 + 1
      idx0 = idx1 - 1    '29/2/2008
      'cutoff(1) = interpQ(Schfor, IOTF(idx1, 0), IOTF(idx2, 0), IOTF(idx3, 0), IOTF(idx1, 1), IOTF(idx2, 1), IOTF(idx3, 1))  'was quadratic interpolation
      'cutoff(2) = interpQ(Schfor, IOTF(idx1, 0), IOTF(idx2, 0), IOTF(idx3, 0), IOTF(idx1, 2), IOTF(idx2, 2), IOTF(idx3, 2))
      'cutoff(3) = interpQ(Schfor, IOTF(idx1, 0), IOTF(idx2, 0), IOTF(idx3, 0), IOTF(idx1, 3), IOTF(idx2, 3), IOTF(idx3, 3))
      'cutoff(4) = interpQ(Schfor, IOTF(idx1, 0), IOTF(idx2, 0), IOTF(idx3, 0), IOTF(idx1, 4), IOTF(idx2, 4), IOTF(idx3, 4))
      'cutoff(5) = interpQ(Schfor, IOTF(idx1, 0), IOTF(idx2, 0), IOTF(idx3, 0), IOTF(idx1, 5), IOTF(idx2, 5), IOTF(idx3, 5))
      cutoff(1) = interpC(Schfor, IOTF(idx0, 0), IOTF(idx1, 0), IOTF(idx2, 0), IOTF(idx3, 0), IOTF(idx0, 1), IOTF(idx1, 1), IOTF(idx2, 1), IOTF(idx3, 1))   '29/2/2008 change to cubic by including idx0
      cutoff(2) = interpC(Schfor, IOTF(idx0, 0), IOTF(idx1, 0), IOTF(idx2, 0), IOTF(idx3, 0), IOTF(idx0, 2), IOTF(idx1, 2), IOTF(idx2, 2), IOTF(idx3, 2))   '29/2/2008 including idx0
      cutoff(3) = interpC(Schfor, IOTF(idx0, 0), IOTF(idx1, 0), IOTF(idx2, 0), IOTF(idx3, 0), IOTF(idx0, 3), IOTF(idx1, 3), IOTF(idx2, 3), IOTF(idx3, 3))   '29/2/2008 including idx0
      cutoff(4) = interpC(Schfor, IOTF(idx0, 0), IOTF(idx1, 0), IOTF(idx2, 0), IOTF(idx3, 0), IOTF(idx0, 4), IOTF(idx1, 4), IOTF(idx2, 4), IOTF(idx3, 4))   '29/2/2008 including idx0
      cutoff(5) = interpC(Schfor, IOTF(idx0, 0), IOTF(idx1, 0), IOTF(idx2, 0), IOTF(idx3, 0), IOTF(idx0, 5), IOTF(idx1, 5), IOTF(idx2, 5), IOTF(idx3, 5))   '29/2/2008 including idx0
   End If
Else
   cutoff(1) = IOTF(idx1, 1)
   cutoff(2) = IOTF(idx1, 2)
   cutoff(3) = IOTF(idx1, 3)
   cutoff(4) = IOTF(idx1, 4)
   cutoff(5) = IOTF(idx1, 5)
End If

Exit Sub
E:
'MsgBox ("problem in BinarySearchI"), 48, "LMSgrowth"  '10/9/2004 remove
End Sub



Function interpC(t As Single, t0 As Single, t1 As Single, t2 As Single, t3 As Single, y0 As Single, y1 As Single, y2 As Single, y3 As Single) As Single
'29/2/2008 cubic interpolation
'note all y are based original age, this must be called after CalcVelocity in cmdFit

Dim tt0 As Single, tt1 As Single, tt2 As Single, tt3 As Single, t01 As Single, t02 As Single, t03 As Single, t12 As Single, t13 As Single, t23 As Single
Dim dt As Single, a0 As Single, a1 As Single, a2 As Single, a3 As Single

tt0 = t - t0: tt1 = t - t1: tt2 = t - t2: tt3 = t - t3
t01 = t0 - t1: t02 = t0 - t2: t03 = t0 - t3
t12 = t1 - t2: t13 = t1 - t3
t23 = t2 - t3

'Huiqi 's test, same as cubic interpolation-------
If y0 = y1 And y1 = y2 And y2 = y3 Then
  interpC = y1 '10/3/2004 add for constant curve, as cubic interpolation will turn to not constant
Else
   'quadratic
   'interpC = y1 * tt2 * tt3 / t12 / t13 - y2 * tt3 * tt1 / t23 / t12 + y3 * tt1 * tt2 / t23 / t13
   'cubic of HP
   interpC = y0 * tt1 * tt2 * tt3 / t01 / t02 / t03 - y1 * tt0 * tt2 * tt3 / t01 / t12 / t13 + y2 * tt0 * tt1 * tt3 / t02 / t12 / t23 - y3 * tt0 * tt1 * tt2 / t03 / t13 / t23
End If
End Function
Function interpQ(a As Single, a1 As Single, a2 As Single, a3 As Single, y1 As Single, y2 As Single, y3 As Single) As Single
'29/2/2008 change it to cubic interpolation -> interoCP
'28/2/2005 quadratic interpolation, copy from LMS & modify,
'note all y are based original age, this must be called after CalcVelocity in cmdFit

Dim tt1 As Single, tt2 As Single, tt3 As Single, t12 As Single, t13 As Single, t23 As Single
tt1 = a - a1: tt2 = a - a2: tt3 = a - a3
t12 = a1 - a2: t13 = a1 - a3: t23 = a2 - a3
If y1 = y2 And y2 = y3 Then
  interpQ = y1 '10/3/2004 add for constant curve, as cubic interpolation will turn to not constant
Else
  interpQ = y1 * tt2 * tt3 / t12 / t13 - y2 * tt3 * tt1 / t23 / t12 + y3 * tt1 * tt2 / t23 / t13
End If
End Function
Function interpL(t As Single, t1 As Single, t2 As Single, y1 As Single, y2 As Single) As Single
'28/2/2005 linear interpolation, copy from LMS and modify, t1<> t2 was checked before call
interpL = y1 + (t - t1) * (y2 - y1) / (t2 - t1)  'linear inperpolation
End Function

Function SDS(sexRange As Variant, tRange As Variant, Yrange As Variant, Mea As String) As Variant
'keep old function of Tim !!!!! 8/3/2005
Dim LL As Single, MM As Single, SS As Single
'Dim cols As Integer, t As Single, y As Single, DataFile As String, AgeCol As String, MeaCol As String  'remove 18/3/2002
Dim cols As Integer, t As Single, Y As Single, AgeCol As String, MeaCol As String
Dim ScrFail As Integer, DataAgeCol As String, DataMeaCol As String, DefFile As String

'On Error Resume Next
On Error GoTo E
SDS = unknown   '15/9/2004 move from the bottom
   'DefFile = "LMSDATA.XLS"   '7/4/2003
   DefFile = "BRITISH1990.XLS"     '25/11/2004
   AgeCol = "AgeLMS"
   Select Case UCase(Mea)
         Case "HT"
              MeaCol = "HTLMS"
         Case "WT"
              MeaCol = "WTLMS"
         Case "BMI"
              MeaCol = "BMILMS"
         Case "HC"
              MeaCol = "HCLMS"
         Case "SH"
              MeaCol = "SHLMS"
         Case "LL"
              MeaCol = "LLLMS"
         Case "WA"
              MeaCol = "WALMS"    '25/11/2004 for waist
         Case Else
              'MsgBox ("Measurement name missing"), 48, "LMSgrowth"   'remove 15/9/2004
              Exit Function
    End Select

'on 7/4/2003 use DefFile to replace DataFile
If IsBookOpen(DefFile) = False Then  'was DataFile = "LMSDATA.XLS"
   If Not IsDiskFile(DefFile) Then
      'MsgBox ("File does not exist")
      'MsgBox ("BRITISH1990.XLS does not exist"), 48, "LMSgrowth"  'remove 15/9/2004
      Exit Function
   Else
      Workbooks.Open DefFile
   End If
End If
If IsNameExist(AgeCol, DefFile) = False Then
   'MsgBox ("Age name not exist"), 48, "LMSgrowth"  'remove 15/9/2004
   Exit Function
End If
If IsNameExist(MeaCol, DefFile) = False Then
   'MsgBox ("Measurement name not exist"), 48, "LMSgrowth"  'remove 15/9/2004
   Exit Function
End If
DataAgeCol = DefFile & "!" & AgeCol
DataMeaCol = DefFile & "!" & MeaCol

'check sex
    If IsMissing(sexRange) = True Then
       GoTo E
    End If
    If sexRange = "" Then
        GoTo E
    End If
    If (Not IsNumeric(sexRange)) Then
        If sexRange = "M" Or sexRange = "m" Then
           cols = 3
        Else
          If sexRange = "F" Or sexRange = "f" Then
             cols = 6
          Else
             GoTo E
          End If
        End If
    Else
       If sexRange = 1 Then
          cols = 3
       Else
          If sexRange = 2 Then
             cols = 6
          Else
             GoTo E
          End If
       End If
    End If
 'Check age
    If IsMissing(tRange) = True Then
        GoTo E
    End If
    'If (IsNull(tRange)) Then
    If tRange = "" Then
        GoTo E
    End If
    If (Not IsNumeric(tRange)) Then
        GoTo E
    End If
    t = tRange
    If (t < -0.326) Or (t > 23) Then
        GoTo E
    End If
'check yy
    If IsMissing(Yrange) Then
        GoTo E
    End If
    If Yrange = "" Then
        GoTo E
    End If
    If (Not IsNumeric(Yrange)) Then
        GoTo E
    End If
Y = Yrange
If Y <= 0 Then GoTo E
BinarySearch t, DataAgeCol, DataMeaCol, cols, LL, MM, SS, ScrFail
If ScrFail = 1 Then
   GoTo E
End If
If LL = 1 Then
   SDS = (Y / MM - 1) / SS
Else
   If LL <> 0 Then
      SDS = (Exp(LL * (Log(Y / MM))) - 1) / (LL * SS)  'not VBA's log = Excel's =Application.LN
   Else
      SDS = (Log(Y / MM)) / SS
   End If
End If
'If Abs(SDS) >= Zcutoff Then GoTo E 'dd->E 15/9/2004   'remove 6/3/2009
'SDS = Format(SDS, "#0.00")   'eg 12.295 -> 12.30   13/5/2003
'SDS = Round(SDS, 3)      'eg 12.295 -> 12.3  22/5/2003 , Round function is not available in Mac
SDS = Int(SDS * 1000 + 0.5) / 1000   '10/6/2003

Exit Function

E:
'MsgBox "problem in SDS", 48, "LMSgrowth"  'remove 15/9/2004
End Function























Sub getItemCol(mycob As ComboBox, n1 As Integer, n2 As Integer)
Dim i As Integer, tmp As String
'AddItems to measures or SDS cols
mycob.Clear
mycob.Style = 2
mycob.BoundColumn = 1
mycob.AddItem ""    'listIndex = 0
'For i = 1 To 256   'A - IV, total 256 columns
For i = n1 To n2    '21/2/2005
    mycob.AddItem ColName(i)
Next i
End Sub

Sub getItemRf(mycob As ComboBox, err As Integer)
'add items to reference combobox
Dim i As Integer
On Error GoTo E
err = 0
mycob.Clear
mycob.Style = 2
mycob.BoundColumn = 1
For i = 1 To RfTotal
    If UCase(RfFiles(i)) = UCase(DataFile) Then RfCurIndex = i - 1
    mycob.AddItem RfFiles(i)
Next i
Exit Sub
E:
err = 1

End Sub


Function IsBookOpen(ByVal BName As String) As Boolean
'return True if book is open
Dim aBook As Object
IsBookOpen = False  'assume failure
BName = Trim(BName)
For Each aBook In Workbooks
    If StrComp(aBook.Name, BName, TXTCOMP) = STREQUAL Then
       IsBookOpen = True
       Exit For
    End If
Next aBook
End Function
Sub RankHead()
'2/5/2003 re-order name of Head if OKHWB = 1 * HWB(4) <>0
Dim k As Integer, n As Integer
n = 4
If HWB(4) <> n Then 'move height to the first
   k = HWB(4): HWB(4) = n: HWB(invHWB(n)) = k    '17/8/2005
   RankSwitch k, n  '17/8/2005
End If
End Sub

Sub RankHW()
'26/6/2003 re-order names for ht & wt
Dim k As Integer, n As Integer
n = 1
If HWB(1) <> n Then 'move height to the first
   k = HWB(1): HWB(1) = n: HWB(invHWB(n)) = k    '17/8/2005
   RankSwitch k, n  '17/8/2005
End If
n = 2
If HWB(2) <> n Then 'move weight to the second
   k = HWB(2): HWB(2) = n: HWB(invHWB(n)) = k    '17/8/2005
   RankSwitch k, n  '17/8/2005
   WTat = 2
End If

End Sub
Sub RankHWB()
'29/4/2003 re-order names
Dim k As Integer, n As Integer
n = 1
If HWB(1) <> n Then 'move height to the first
   k = HWB(1): HWB(1) = n: HWB(invHWB(n)) = k    '17/8/2005
   RankSwitch k, n  '17/8/2005
End If
n = 2
If HWB(2) <> n Then 'move weight to the second
   k = HWB(2): HWB(2) = n: HWB(invHWB(n)) = k    '17/8/2005
   RankSwitch k, n  '17/8/2005
   WTat = 2
End If
n = 3
If HWB(3) <> n Then 'move BMI to the third
   k = HWB(3): HWB(3) = n: HWB(invHWB(n)) = k    '17/8/2005
   RankSwitch k, n  '17/8/2005
End If
mUnit(3) = "kglm2"    '8/8/2007 kg/m2->kglm2

End Sub

Sub removeSP(Sname As String)
'10/7/2003
Dim n As Integer, s As String, SS As String
n = 1: s = Sname: SS = ""
While n > 0
   n = InStr(s, " ")
   If n = 0 Then
      SS = SS & s
      GoTo dd
   End If
   SS = SS & Mid(s, 1, n - 1)
   Sname = Mid(s, n + 1, Len(s) - n + 1)
   s = Sname
Wend
dd:
Sname = SS
End Sub




Sub FNCYMWD(idex As Integer, iSex As Integer)

'21/6/2007 copy from SDSYMWD and modify for lung
Dim j1 As Integer, j2 As Integer, j3 As Integer, j4 As Integer, j5 As Integer, j6 As Integer, cur As String, tmpName As String, tmpaName As String, tmpDfile As String, tmptunit As String, DaRow1_c_adj As Long  '24/1/2005
Dim tmpDAgeU As String, i As Long, Rt As Long
On Error GoTo E
cur = ColName(idxM2_c(idex))   'use 256 columns
SetColFormat cur        '9/11/2007
If NHead_c = 1 Then
   DaRow1_c_adj = DaRow1_c + 1
   'Range(cur & DaRow1_c).value = "SDS_" & mTitle(idex)   '4/3/2005
   Range(cur & DaRow1_c).value = FNClist(Fidx) & "_" & mTitle(idex)   '4/3/2005, 22/6/2007
Else
   DaRow1_c_adj = DaRow1_c        '24/1/2005 add to adjust Head option
End If
If DaRow1_c_adj > DaRow2_c Then Exit Sub   '24/1/2005
j1 = idxSex_c - 1 - idxM2_c(idex)
If Datetype_c = 0 Then j2 = idxAge_c - idxM2_c(idex) Else j2 = idxAgeD_c - idxM2_c(idex)  '2/2/2005
j3 = idxM1_c(idex) - idxM2_c(idex)
'Range(cur & DaRow1_c_adj).Select   '24/1/2005, 24/7/2007 move to bottom
tmpName = Chr(34) & mName(idex) & Chr(34)  '17/11/2004
tmpDfile = Chr(34) & DataFile & Chr(34)    '23/11/2004
tmpaName = Chr(34) & tName & Chr(34)       '29/11/2004
tmpDAgeU = Chr(34) & frmSDSCov!lblAgeU.Caption & Chr(34)       '7/3/2005
Rt = Range(DataFile & "!" & mName(idex)).Row   '19/12/2008

Dim Ssex As Variant  '4/3/2005
Select Case iSex     '4/3/2005
   Case 0
        Ssex = Chr(34) & "M" & Chr(34)
   Case 1
        Ssex = Chr(34) & "F" & Chr(34)
   Case Is > 1
        Ssex = "RC[" & j1 & "]"
End Select

j5 = idxCov1_c - idxM2_c(idex)
j6 = idxCov2_c - idxM2_c(idex)
'25/7/2007 to solve Mac proble with xlFill
'-----------------------------------------------------
Range(cur & DaRow1_c_adj).Select   '25/7/2007
Select Case idxGest_c
    Case 0  'not use gestation
         For i = DaRow1_c_adj To DaRow2_c
             Range(cur & i).Select
             'ActiveCell.FormulaR1C1 = "=cFNC(" & Fidx & "," & Ssex & ",RC[" & j2 & "]," & tmpDAgeU & ",RC[" & j3 & "]," & tmpaName & "," & tmpName & ", " & tmpDfile & ",RC[" & j5 & "],RC[" & j6 & "])"  'remove 19/12/2008
             If Rt = 10 Then  '19/12/2008
                ActiveCell.FormulaR1C1 = "=cFNC(" & Fidx & "," & Ssex & ",RC[" & j2 & "]," & tmpDAgeU & ",RC[" & j3 & "]," & tmpaName & "," & tmpName & ", " & tmpDfile & ",RC[" & j5 & "])"
             Else
                ActiveCell.FormulaR1C1 = "=cFNC(" & Fidx & "," & Ssex & ",RC[" & j2 & "]," & tmpDAgeU & ",RC[" & j3 & "]," & tmpaName & "," & tmpName & ", " & tmpDfile & ",RC[" & j5 & "],RC[" & j6 & "])"
             End If
         Next i
    Case Is > 0
         j4 = idxGest_c - idxM2_c(idex)
         For i = DaRow1_c_adj To DaRow2_c
             Range(cur & i).Select
             'ActiveCell.FormulaR1C1 = "=cFNCg(" & Fidx & "," & Ssex & ",RC[" & j4 & "], RC[" & j2 & "]," & tmpDAgeU & ",RC[" & j3 & "], " & tmpaName & "," & tmpName & ", " & tmpDfile & ",RC[" & j5 & "],RC[" & j6 & "])"   'remove 19/12/2008
             If Rt = 10 Then  '19/12/2008
                ActiveCell.FormulaR1C1 = "=cFNCg(" & Fidx & "," & Ssex & ",RC[" & j4 & "], RC[" & j2 & "]," & tmpDAgeU & ",RC[" & j3 & "], " & tmpaName & "," & tmpName & ", " & tmpDfile & ",RC[" & j5 & "])"
             Else
                ActiveCell.FormulaR1C1 = "=cFNCg(" & Fidx & "," & Ssex & ",RC[" & j4 & "], RC[" & j2 & "]," & tmpDAgeU & ",RC[" & j3 & "], " & tmpaName & "," & tmpName & ", " & tmpDfile & ",RC[" & j5 & "],RC[" & j6 & "])"
             End If
         Next i
End Select
Exit Sub    'test for Mac
'-----------------------------------------------------
'25/7/2007 remove previous code, keep
'-----------------------------------------------------
Range(cur & DaRow1_c_adj).Select   '25/7/2007 move from above
Select Case idxGest_c
    Case 0  'not use gestation
         'ActiveCell.FormulaR1C1 = "=cFNC(" & Fidx & "," & Ssex & ",RC[" & j2 & "]," & tmpDAgeU & ",RC[" & j3 & "]," & tmpaName & "," & tmpName & ", " & tmpDfile & ",RC[" & j5 & "],RC[" & j6 & "])"   'remove 19/12/2008
         If Rt = 10 Then
            ActiveCell.FormulaR1C1 = "=cFNC(" & Fidx & "," & Ssex & ",RC[" & j2 & "]," & tmpDAgeU & ",RC[" & j3 & "]," & tmpaName & "," & tmpName & ", " & tmpDfile & ",RC[" & j5 & "])"
         Else
            ActiveCell.FormulaR1C1 = "=cFNC(" & Fidx & "," & Ssex & ",RC[" & j2 & "]," & tmpDAgeU & ",RC[" & j3 & "]," & tmpaName & "," & tmpName & ", " & tmpDfile & ",RC[" & j5 & "],RC[" & j6 & "])"
         End If
    Case Is > 0
         j4 = idxGest_c - idxM2_c(idex)
         'ActiveCell.FormulaR1C1 = "=cFNCg(" & Fidx & "," & Ssex & ",RC[" & j4 & "], RC[" & j2 & "]," & tmpDAgeU & ",RC[" & j3 & "], " & tmpaName & "," & tmpName & ", " & tmpDfile & ",RC[" & j5 & "],RC[" & j6 & "])"   'remove 19/12/2008
         If Rt = 10 Then
            ActiveCell.FormulaR1C1 = "=cFNCg(" & Fidx & "," & Ssex & ",RC[" & j4 & "], RC[" & j2 & "]," & tmpDAgeU & ",RC[" & j3 & "], " & tmpaName & "," & tmpName & ", " & tmpDfile & ",RC[" & j5 & "])"
         Else
            ActiveCell.FormulaR1C1 = "=cFNCg(" & Fidx & "," & Ssex & ",RC[" & j4 & "], RC[" & j2 & "]," & tmpDAgeU & ",RC[" & j3 & "], " & tmpaName & "," & tmpName & ", " & tmpDfile & ",RC[" & j5 & "],RC[" & j6 & "])"
         End If
End Select
If DaRow2_c > DaRow1_c_adj Then   '24/1/2005
   Range(cur & DaRow1_c_adj).Select
   'Selection.NumberFormat = "0.00"   '31/3/2005 note the format will not be removed if you simply delete values, remove 29/11/2005
   Selection.AutoFill Destination:=Range(cur & DaRow1_c_adj & ":" & cur & DaRow2_c), Type:=xlFillDefault
End If
'-----------------------------------------------------

Exit Sub

E:
'MsgBox "Error in FUNYMWD.", 48, "LMSgrowth"  'remove 15/9/2004
End Sub

Sub SDSYMWD(idex As Integer, iSex As Integer)

'17/11/2004, 3/12/2004 modify for gestation, 24/1/2005 modified
Dim j1 As Integer, j2 As Integer, j3 As Integer, j4 As Integer, j5 As Integer, j6 As Integer, cur As String, tmpName As String, tmpaName As String, tmpDfile As String, tmptunit As String, DaRow1_s_adj As Long  '24/1/2005
Dim tmpDAgeU As String      '7/3/2005 data age unit
On Error GoTo E
cur = ColName(idxM2_s(idex))   'use 256 columns
SetColFormat cur        '9/11/2007
If NHead_s = 1 Then
   DaRow1_s_adj = DaRow1_s + 1
   Range(cur & DaRow1_s).value = "SDS_" & mTitle(idex)   '4/3/2005
Else
   DaRow1_s_adj = DaRow1_s        '24/1/2005 add to adjust Head option
End If
If DaRow1_s_adj > DaRow2_s Then Exit Sub   '24/1/2005
j1 = idxSex_s - 1 - idxM2_s(idex)
If Datetype_s = 0 Then j2 = idxAge_s - idxM2_s(idex) Else j2 = idxAgeD_s - idxM2_s(idex)  '2/2/2005
j3 = idxM1_s(idex) - idxM2_s(idex)
'cur = ColName(idxM2_s(idex))   'use 256 columns, 4/3/2005 move to top
Range(cur & DaRow1_s_adj).Select   '24/1/2005
tmpName = Chr(34) & mName(idex) & Chr(34)  '17/11/2004
tmpDfile = Chr(34) & DataFile & Chr(34)    '23/11/2004
tmpaName = Chr(34) & tName & Chr(34)       '29/11/2004
'tmptunit = Chr(34) & tUnit & Chr(34)       '3/12/2004
tmpDAgeU = Chr(34) & frmSDSFx!lblAgeU.Caption & Chr(34)       '7/3/2005
Dim Ssex As Variant  '4/3/2005
Select Case iSex     '4/3/2005
   Case 0
        Ssex = Chr(34) & "M" & Chr(34)
   Case 1
        Ssex = Chr(34) & "F" & Chr(34)
   Case Is > 1
        Ssex = "RC[" & j1 & "]"
End Select

Select Case idxGest_s   '4/3/2005
    Case 0  'not use gestation
         ActiveCell.FormulaR1C1 = "=cSDS(" & Ssex & ",RC[" & j2 & "]," & tmpDAgeU & ",RC[" & j3 & "]," & tmpaName & "," & tmpName & ", " & tmpDfile & ")"
    Case Is > 0
         j4 = idxGest_s - idxM2_s(idex)
         ActiveCell.FormulaR1C1 = "=cSDSg(" & Ssex & ",RC[" & j4 & "], RC[" & j2 & "]," & tmpDAgeU & ",RC[" & j3 & "], " & tmpaName & "," & tmpName & ", " & tmpDfile & ")"   '7/3/2005 remove tmptunit
End Select

If DaRow2_s > DaRow1_s_adj Then   '24/1/2005
   Range(cur & DaRow1_s_adj).Select
   'Selection.NumberFormat = "0.00"   '31/3/2005 note the format will not be removed if you simply delete values, remove 29/11/2005
   Selection.AutoFill Destination:=Range(cur & DaRow1_s_adj & ":" & cur & DaRow2_s), Type:=xlFillDefault
End If
Exit Sub

E:
'MsgBox "Error in SDSYMWD.", 48, "LMSgrowth"  'remove 15/9/2004
End Sub
Sub SDYMWD(idex As Integer, iSex As Integer)

'24/7/2007 copy from SDSYMWD
Dim j1 As Integer, j2 As Integer, j3 As Integer, j4 As Integer, j5 As Integer, j6 As Integer, cur As String, tmpName As String, tmpaName As String, tmpDfile As String, tmptunit As String, DaRow1_s_adj As Long  '24/1/2005
Dim tmpDAgeU As String      '7/3/2005 data age unit
On Error GoTo E
cur = ColName(idxM2_s(idex))   'use 256 columns
SetColFormat cur        '9/11/2007
If NHead_s = 1 Then
   DaRow1_s_adj = DaRow1_s + 1
   'Range(cur & DaRow1_s).value = "SDS_" & mTitle(idex)   '4/3/2005
   Range(cur & DaRow1_s).value = FNClist(Fidx) & "_" & mTitle(idex)   '4/3/2005, 25/7/2007
Else
   DaRow1_s_adj = DaRow1_s        '24/1/2005 add to adjust Head option
End If
If DaRow1_s_adj > DaRow2_s Then Exit Sub   '24/1/2005
j1 = idxSex_s - 1 - idxM2_s(idex)
If Datetype_s = 0 Then j2 = idxAge_s - idxM2_s(idex) Else j2 = idxAgeD_s - idxM2_s(idex)  '2/2/2005
j3 = idxM1_s(idex) - idxM2_s(idex)
'cur = ColName(idxM2_s(idex))   'use 256 columns, 4/3/2005 move to top
Range(cur & DaRow1_s_adj).Select   '24/1/2005
tmpName = Chr(34) & mName(idex) & Chr(34)  '17/11/2004
tmpDfile = Chr(34) & DataFile & Chr(34)    '23/11/2004
tmpaName = Chr(34) & tName & Chr(34)       '29/11/2004
'tmptunit = Chr(34) & tUnit & Chr(34)       '3/12/2004
tmpDAgeU = Chr(34) & frmSDSFx!lblAgeU.Caption & Chr(34)       '7/3/2005
Dim Ssex As Variant  '4/3/2005
Select Case iSex     '4/3/2005
   Case 0
        Ssex = Chr(34) & "M" & Chr(34)
   Case 1
        Ssex = Chr(34) & "F" & Chr(34)
   Case Is > 1
        Ssex = "RC[" & j1 & "]"
End Select

Select Case idxGest_s   '4/3/2005
    Case 0  'not use gestation
         ActiveCell.FormulaR1C1 = "=cSD(" & Fidx & "," & Ssex & ",RC[" & j2 & "]," & tmpDAgeU & ",RC[" & j3 & "]," & tmpaName & "," & tmpName & ", " & tmpDfile & ")"
    Case Is > 0
         j4 = idxGest_s - idxM2_s(idex)
         ActiveCell.FormulaR1C1 = "=cSDg(" & Fidx & "," & Ssex & ",RC[" & j4 & "], RC[" & j2 & "]," & tmpDAgeU & ",RC[" & j3 & "], " & tmpaName & "," & tmpName & ", " & tmpDfile & ")"   '7/3/2005 remove tmptunit
End Select

If DaRow2_s > DaRow1_s_adj Then   '24/1/2005
   Range(cur & DaRow1_s_adj).Select
   'Selection.NumberFormat = "0.00"   '31/3/2005 note the format will not be removed if you simply delete values, remove 29/11/2005
   Selection.AutoFill Destination:=Range(cur & DaRow1_s_adj & ":" & cur & DaRow2_s), Type:=xlFillDefault
End If
Exit Sub

E:
'MsgBox "Error in SDSYMWD.", 48, "LMSgrowth"  'remove 15/9/2004
End Sub













Function ShortName(s As String) As String
s = Trim(s)
'If Len(s) > 6 Then ShortName = Mid(s, 1, 6) Else ShortName = s
If Len(s) > 9 Then ShortName = Mid(s, 1, 8) Else ShortName = s     '2/8/2007, 18/12/2008 8->9
End Function





Function IsDiskFile(fname As String) As Boolean
'return True if fName is found on disk, False otherwise
If (Dir(fname) <> "") Then
    IsDiskFile = True
Else
    IsDiskFile = False
End If
End Function

Function IsNameExist(ByVal nName As String, Dfile As String) As Boolean
'return True if book is open
Dim aName As Name
IsNameExist = False  'assume failure
nName = Trim(nName)
For Each aName In Workbooks(Dfile).Names
    If StrComp(aName.Name, nName, TXTCOMP) = STREQUAL Then
       IsNameExist = True
       Exit For
    End If
Next aName
End Function


Function CENTILE(sexRange As Variant, tRange As Variant, Yrange As Variant, Mea As String) As Variant
'keep old function of Tim !!!!! 8/3/2005
Dim LL As Single, MM As Single, SS As Single
Dim cols As Integer, t As Single, Y As Single, AgeCol As String, MeaCol As String
Dim ScrFail As Integer, DataAgeCol As String, DataMeaCol As String, DefFile As String

'On Error Resume Next
On Error GoTo E
CENTILE = unknown   '15/9/2004
   'DefFile = "LMSDATA.XLS"   '7/4/2003
   DefFile = "BRITISH1990.XLS"     '25/11/2004
   AgeCol = "AgeLMS"
   Select Case UCase(Mea)
         Case "HT"
              MeaCol = "HTLMS"
         Case "WT"
              MeaCol = "WTLMS"
         Case "BMI"
              MeaCol = "BMILMS"
         Case "HC"
              MeaCol = "HCLMS"
         Case "SH"
              MeaCol = "SHLMS"
         Case "LL"
              MeaCol = "LLLMS"
         Case "WA"
              MeaCol = "WALMS"    '25/11/2004 for waist
         Case Else
              'MsgBox ("Measurement name missing"), 48, "LMSgrowth"  'remove 15/9/2004
              Exit Function
    End Select

'check LMSdata.xls, 7/4/2003 use DefFile to replace LMSDATA.xls
If IsBookOpen(DefFile) = False Then  'was DataFile = "LMSDATA.XLS"
   If Not IsDiskFile(DefFile) Then
      'MsgBox ("LMSDATA.XLS does not exist"), 48, "LMSgrowth"   'remove 15/9/2004
      Exit Function
   Else
      Workbooks.Open DefFile  'was in Sub Binarysearch
   End If
End If
If IsNameExist(AgeCol, DefFile) = False Then
   'MsgBox ("Age name not exist"), 48, "LMSgrowth"  'remove 15/9/2004
   Exit Function
End If
If IsNameExist(MeaCol, DefFile) = False Then
   'MsgBox ("Measurement name not exist"), 48, "LMSgrowth"  'remove 15/9/2004
   Exit Function
End If
DataAgeCol = DefFile & "!" & AgeCol
DataMeaCol = DefFile & "!" & MeaCol
'check sex
    If IsMissing(sexRange) = True Then
       GoTo E
    End If
    If sexRange = "" Then
        GoTo E
    End If
    If (Not IsNumeric(sexRange)) Then
        If sexRange = "M" Or sexRange = "m" Then
           cols = 3
        Else
          If sexRange = "F" Or sexRange = "f" Then
             cols = 6
          Else
             GoTo E
          End If
        End If
    Else
       If sexRange = 1 Then
          cols = 3
       Else
          If sexRange = 2 Then
             cols = 6
          Else
             GoTo E
          End If
       End If
    End If
'Check age
    If IsMissing(tRange) = True Then
        GoTo E
    End If
    If tRange = "" Then
        GoTo E
    End If
    If (Not IsNumeric(tRange)) Then
        GoTo E
    End If
    t = tRange
    If (t < -0.326) Or (t > 23) Then
        GoTo E
    End If
'check yy
    If IsMissing(Yrange) Then
        GoTo E
    End If
    If Yrange = "" Then
        GoTo E
    End If
    If (Not IsNumeric(Yrange)) Then
        GoTo E
    End If
Y = Yrange
'If Abs(Y) >= Zcutoff Then GoTo E   'remove 6/3/2009
BinarySearch t, DataAgeCol, DataMeaCol, cols, LL, MM, SS, ScrFail
If ScrFail = 1 Then
   GoTo E
End If
If LL = 1 Then
   CENTILE = 1 + SS * Y
Else
   If LL <> 0 Then
      CENTILE = (1 + LL * SS * Y) ^ (1 / LL) 'not VBA's log = Excel's =Application.LN
   Else
      CENTILE = Exp(SS * Y)
   End If
End If
CENTILE = CENTILE * MM
'CENTILE = Format(CENTILE, "#######0.00")   'eg 12.295 -> 12.3  13/5/2003
'CENTILE = Round(CENTILE, 3)     'eg 12.30->12.3  22/5/2003, Round function is not available in Mac
CENTILE = Int(CENTILE * 1000 + 0.5) / 1000 '10/6/2003

Exit Function
E:
'MsgBox "problem in CENTILE", 48, "LMSgrowth"
End Function












Sub OpenGain()

Dim err As Integer
'err = 0
Application.ScreenUpdating = False
On Error GoTo E
CPU = Application.OperatingSystem    '4/6/2003 move from Auto_open
PS = Application.PathSeparator
If CPU = "Mac" Then ZoomSize = ZoomMac Else ZoomSize = ZoomPC
If NOpenRf < 1 Then  '15/5/2003
   getExistingXY err     '20/6/2003
   If err = 1 Then GoTo E
   ZPInit     '16/5/2005
   ZPopen     '16/5/2005
   NOpenRf = NOpenRf + 1
End If
If OkAge = 0 Then GoTo E     '16/5/2003
If OkWT = 1 Then frmWtGainCo.Show Else MsgBox ("Weight reference is not available for the selected references."), 48, "LMSgrowth"
 
Application.ScreenUpdating = True
Exit Sub

E:
'MsgBox "Calculation of weight gain is not available for the selected references.", 48, "LMSgrowth"  '25/11/2004
Application.ScreenUpdating = True
End Sub



Sub OpenOneChild()
Dim err As Integer

'err = 0
Application.ScreenUpdating = False
On Error GoTo E
CPU = Application.OperatingSystem    '4/6/2003 move from Auto_open
PS = Application.PathSeparator
If CPU = "Mac" Then ZoomSize = ZoomMac Else ZoomSize = ZoomPC
If NOpenRf < 1 Then  '15/5/2003
   getExistingXY err     '20/6/2003
   If err = 1 Then GoTo E
   ZPInit     '16/5/2005
   ZPopen     '16/5/2005
   NOpenRf = NOpenRf + 1
End If
If OkAge = 0 Then
   MsgBox "Calculator is not available for the selected references.", 48, "LMSgrowth"   '16/5/2005
   GoTo E  '16/5/2003
End If
If idxLLN = 0 Then idxLLN = 6   '5/4/2011
getFNClist   '3/8/2007
If NumCov > 0 Then frmOneChildCov.Show Else frmOneChildFx.Show   '8/6/2007
Application.ScreenUpdating = True
Exit Sub

E:
Application.ScreenUpdating = True
End Sub

Sub OpenSDS()

Dim err As Integer, tmpcol As Integer
'err = 0
Application.ScreenUpdating = False
On Error GoTo E
CPU = Application.OperatingSystem    '4/6/2003 move from Auto_open
PS = Application.PathSeparator
If CPU = "Mac" Then ZoomSize = ZoomMac Else ZoomSize = ZoomPC
If NOpenRf < 1 Then  '15/5/2003
   getExistingXY err     '20/6/2003
   If err = 1 Then GoTo E
   ZPInit     '16/5/2005
   ZPopen     '16/5/2005
   NOpenRf = NOpenRf + 1
End If
getFNClist    '25/7/2007
'frmSDSFx.Show   '25/11/2004
If NumCov > 0 Then frmSDSCov.Show Else frmSDSFx.Show   '21/5/2007, 8/6/2007
Application.ScreenUpdating = True
Exit Sub
E:
Application.ScreenUpdating = True
End Sub


Sub DeleteMenu()
    On Error Resume Next
    'Application.ScreenUpdating = False
     MenuBars(xlWorksheet).Menus("LMSgrowth").Delete   '28/3/2003
    'MenuBars(xlNoDocuments).Menus("XLStatistics").Delete
    'MenuBars(xlChart).Menus("XLStatistics").Delete
   
End Sub
Sub MakeMenu()
    On Error Resume Next
    'DeleteMenu
    Set M = MenuBars(xlWorksheet)
    getIOTFRf     '29/11/2004 move from OpenIOTF
    getIOTFm      '23/4/2007 to add thinness for male, keep getIOTFRf for old results re-frash
    getIOTFf      '23/4/2007 to add thinness for female, keep getIOTFRf for old results re-frash
    GetColName    '14/12/2004 move from all form initialize
    getFNClist    '25/7/2007
    getNameLLN    '25/3/2011
    'idxDec_P = 2  '29/11/2005 default for 0,1,2,3, 9/11/2007 remove
    'ZPinit       '15/12/2004  'remove 17/3/2005, call in frmZP
    MakeMenuW
    'Set M = MenuBars(xlNoDocuments)
    'MakeMenuND
    'Set M = MenuBars(xlChart)
    'MakeMenuC
End Sub
Sub MakeMenuW()
    With M
        .Menus.add Caption:="LMSgrowth"  '1/12/2001
        With .Menus("LMSgrowth")   '1/12/2001
            .MenuItems.add Caption:="Calculator", OnAction:="OpenOneChild"
            .MenuItems.add Caption:="Measurement to/from SDS", OnAction:="OpenSDS"
            .MenuItems.add Caption:="Centiles", OnAction:="OpenZP"
            .MenuItems.add Caption:="Weight Gain to SDS", OnAction:="OpenGain"
            .MenuItems.add Caption:="BMI to International Grade", OnAction:="OpenIOTF"
            '.MenuItems.add Caption:="Preferences", OnAction:="OpenPref"    '9/11/2007 remove for decimal
            .MenuItems.add Caption:="Preference", OnAction:="OpenPreference"    '25/3/2011
            .MenuItems.add "-"
            .MenuItems.add Caption:="Select Reference", OnAction:="OpenSelectRf"
            .MenuItems.add Caption:="Create New Reference", OnAction:="OpenNewRf"
            .MenuItems.add Caption:="Modify Old Reference", OnAction:="OpenOldRf"
            .MenuItems.add "-"
            .MenuItems.add Caption:="Help", OnAction:="ShowHelp"
            .MenuItems.add "-"
            .MenuItems.add Caption:="About the LMSgrowth Program", OnAction:="ShowAbout"
        End With
    End With
End Sub









Sub SetFont(myForm As UserForm)
Dim con As Control, myFont As String, mySize As Integer, txt As TextBox, cob As ComboBox
Dim s As String
On Error GoTo E
If CPU = "Mac" Then
   myFont = "Geneva"    '"Geneva", Verdana, Gill Sans, Lucida Grande
   mySize = 9
Else
   myFont = "Tahoma"   'Tahoma for PC, Geneva for Mac
   mySize = 8   '9 for Mac
End If

myForm.Font.Name = myFont
myForm.Font.Size = mySize
For Each con In myForm.Controls
    s = con.Name
    con.Font.Name = myFont
    con.Font.Size = mySize
    con.Font.Bold = False   'Bold in Mac
    
Next con
E:
s = s
End Sub

Sub ShowAbout()
'18/3/2002
Dim msg As String, NL As String
NL = Chr$(10)
msg = "LMSgrowth program version 2.74, compiled on 03 May 2011." & NL & NL
msg = msg & "Authors: Huiqi Pan and Tim Cole" & NL & NL
msg = msg & "Copyright � 2002-11 Medical Research Council, UK" & NL & NL
MsgBox msg, 0, "About the LMSgrowth Program"

End Sub

 
Sub ShowHelp()
On Error GoTo E
CPU = Application.OperatingSystem    '3/5/2007
PS = Application.PathSeparator

getHelp 2     '24/3/2011
'----------------------------remove to getHelp 24/3/2011
'If CPU = "Mac" Then
'   MsgBox (MacHelp1 & Chr(13) & MacHelp2 & Chr(13) & MacHelp3), 48, "LMSgrowth"    '3/5/2007
'Else
'   Application.Help Workbooks("growth.xls").Path & PS & "growth.hlp"   'for me to work in Excel, not work in Add-ins
'   'Application.Help AddIns("growth").Path & PS & "growth.hlp"   'for Add-ins
'End If
'----------------------------remove to getHelp 24/3/2011

Exit Sub
E: MsgBox ("Cannot find Help file."), 48, "LMSgrowth"
End Sub





 












































Sub XLSQuit()
    'DeleteMenu
    'ThisWorkbook.Close SaveChanges:=False
    Workbooks(DataFile).Close SaveChanges:=False  '28/03/2003
End Sub









Sub GetColName()
Dim i As Integer, j As Integer, k As Integer
For j = 1 To 26
    ColName(j) = Chr(64 + j)
Next j
For i = 2 To 9
    For j = 1 To 26
        k = (i - 1) * 26 + j
        ColName(k) = Chr(63 + i) & Chr(64 + j)
    Next j
Next i
For i = 1 To 22  'reserve the 22nd "IV" for calc BMI
    k = k + 1
    ColName(k) = Chr(64 + 9) & Chr(64 + i)
Next i
End Sub








