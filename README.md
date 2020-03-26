# GeologicalSection

Based on the original geological data of borehole, the adjacent relation of borehole is automatically judged 
and the geological section topology is formed.

基于钻孔原始地质数据，自动判断钻孔的相邻关系，并形成地质剖面拓扑。

 ###################################################################################
 
The main differences from the traditional drill section method are as follows:

1. The adjacent borehole used to generate the borehole profile supports customization (by default, the adjacent 
borehole relationship is determined by Voronoi algorithm), and the generated borehole profile can be freely created.

2. After the drilling data is written into the. XLSX file in the sample format, the script can automatically 
generate all adjacent drilling profiles with one key.

3. Can handle the automatic creation of sections of complex geological structure such as lens body and intrusive body.

4. The data structure of the generated borehole section adopts the directed topology diagram [arc number, starting 
number, ending number, left domain number, right domain number], and retains all the topological features of the section.
Compared with the traditional methods, it is beneficial to realize the < automated modeling > of < complex 3d geology > 
in BIM and CIM scenarios.


与传统钻孔剖面图做法的区别主要在于：

1、用于生成钻孔剖面的邻接钻孔支持自定义（默认由Voronoi算法确定钻孔邻接关系），可自由创建生成钻孔剖面。

2、钻孔数据按示例格式写入.xlsx文件后，可由脚本自动一键生成所有邻接钻孔剖面。

3、可以处理透镜体、侵入体等复杂地质结构剖面图的自动化创建。

4、所生成钻孔剖面的数据结构采用有向拓扑图 [弧线号，起点号，终点号，左域号，右域号]，保留了剖面图的全部拓扑特征，
  相比传统方法，有利于实现BIM、CIM场景下的 <复杂三维地质> 的 <自动化建模>。
  
 ###################################################################################



