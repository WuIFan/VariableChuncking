請使用python2.7



!!!!!!!!!!!!!重要!!!!!!!!!!!!!!!!!
在執行mycdc.py前請先將hash.txt刪除
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!



====================================Data Deduplication===============================
執行mycdc.py
會將500A.txt、500B.txt、500C.txt、500D.txt做deduplication
產生hash.txt(用來記錄及查找)
並將做完deduplication的檔案放到dedup資料夾中


===================================  檔  案  復  原  ================================
執行remake.py
可以將deduplication過的檔案復原
放在remake資料夾裡
(程式裡的 WantToRemake="500B.txt"
"500B.txt"可以換成有做deduplication的檔案(例:500A.txt、500B.txt、500C.txt、500D.txt))




!!!!!!!!!!!!!重要!!!!!!!!!!!!!!!!!
在執行mycdc.py前請先將hash.txt刪除
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!