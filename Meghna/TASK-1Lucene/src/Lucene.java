import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map.Entry;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.Fields;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.MultiFields;
import org.apache.lucene.index.Term;
import org.apache.lucene.index.Terms;
import org.apache.lucene.index.TermsEnum;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.BytesRef;
import org.apache.lucene.util.Version;

import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.hssf.usermodel.HSSFSheet;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;

/**
 * To create Apache Lucene index in a folder and add files into this index based
 * on the input of the user.
 */
public class Lucene {
    private static Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_47);
    private static Analyzer sAnalyzer = new SimpleAnalyzer(Version.LUCENE_47);
    static int count=0,totalFrequency = 0;
    static HSSFWorkbook workbook;
	public static LinkedHashMap<String, Integer> sortedTermFreq;
    private IndexWriter writer;
    private ArrayList<File> queue = new ArrayList<File>();

    public static void main(String[] args) throws IOException {
	System.out
		.println("Enter the FULL path where the index will be created: (e.g. /Usr/index or c:\\temp\\index)");

	String indexLocation = null;
	BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
	String s = br.readLine();
	sortedTermFreq = new LinkedHashMap<String, Integer>();
	
	Lucene indexer = null;
	try {
	    indexLocation = s;
	    indexer = new Lucene(s);
	} catch (Exception ex) {
	    System.out.println("Cannot create index..." + ex.getMessage());
	    System.exit(-1);
	}

	// ===================================================
	// read input from user until he enters q for quit
	// ===================================================
	while (!s.equalsIgnoreCase("q")) {
	    try {
		System.out
			.println("Enter the FULL path to add into the index (q=quit): (e.g. /home/mydir/docs or c:\\Users\\mydir\\docs)");
		System.out
			.println("[Acceptable file types: .xml, .html, .html, .txt]");
		s = br.readLine();
		if (s.equalsIgnoreCase("q")) {
		    break;
		}

		// try to add file into the index
		indexer.indexFileOrDirectory(s);
	    } catch (Exception e) {
		System.out.println("Error indexing " + s + " : "
			+ e.getMessage());
	    }
	}

	// ===================================================
	// after adding, we always have to call the
	// closeIndex, otherwise the index is not created
	// ===================================================
	indexer.closeIndex();

	// =========================================================
	// Now search
	// =========================================================
	IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(
		indexLocation)));
	IndexSearcher searcher = new IndexSearcher(reader);
	TopScoreDocCollector collector = TopScoreDocCollector.create(100, true);
	
	Fields f = MultiFields.getFields(reader);
	Terms term = f.terms("contents");
	TermsEnum j = term.iterator(null);
	HashMap<String, Integer> termFrq = new HashMap<String,Integer>(); 
	
	termFrq = populateWordFrequency(reader, j, count, termFrq);
	sortedTermFreq=sortWordFrequency(termFrq,false);
   

	s = "";
	String input = "";
	int q_no=1;
	File file = new File("query.txt");
	workbook = new HSSFWorkbook();
	File folder = new File("lucenefiles");
	folder.mkdir();
		
	try (BufferedReader br1 = new BufferedReader(new FileReader(file))) {
		String line;
		while ((line = br1.readLine()) != null) {
			
			String[] qr = line.split(" ");

			s = String.join(" ",Arrays.copyOfRange(qr, 1,qr.length-1));
			try {
				collector = TopScoreDocCollector.create(100, true);
				System.out.println("query : "+s);

				Query q = new QueryParser(Version.LUCENE_47, "contents",
						sAnalyzer).parse(s);
				searcher.search(q, collector);
				ScoreDoc[] hits = collector.topDocs().scoreDocs;

				
				writeExcelFile(hits,searcher,q_no, "LuceneQuery"+q_no);
				System.out.println("Found " + hits.length + " hits.");
				for (int i = 0; i < hits.length; ++i) {
					int docId = hits[i].doc;
					Document d = searcher.doc(docId);
					System.out.println((i + 1) + ". " + d.get("path")
					+ " score=" + hits[i].score);
				}	
			
				String queryData[] =s.split(" ");
				int termFreq = 0;
				int docCount=0;
				for (int i = 0; i < queryData.length; i++) 
				{  
					Term termInstance = new Term("contents", queryData[i]); 
					termFreq += reader.totalTermFreq(termInstance); 
					docCount += reader.docFreq(termInstance); 
				}
				System.out.println(s + " Term Frequency " + termFreq
						+ " - Document Frequency " + docCount);

			} catch (Exception e) {
				System.out.println("Error searching " + s + " : "
						+e.getMessage());
				e.printStackTrace();
				break;
			}
			count++;
			q_no++;
		}

	}
	try (FileOutputStream outputStream = new FileOutputStream("Lucene.xls")) {
        workbook.write(outputStream);
    }
    }

    /**
     * Constructor
     * 
     * @param indexDir
     *            the name of the folder in which the index should be created
     * @throws java.io.IOException
     *             when exception creating index.
     */
    Lucene(String indexDir) throws IOException {

	FSDirectory dir = FSDirectory.open(new File(indexDir));

	IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47,
		sAnalyzer);

	writer = new IndexWriter(dir, config);
    }

    /**
     * Indexes a file or directory
     * 
     * @param fileName
     *            the name of a text file or a folder we wish to add to the
     *            index
     * @throws java.io.IOException
     *             when exception
     */
    public void indexFileOrDirectory(String fileName) throws IOException {
	// ===================================================
	// gets the list of files in a folder (if user has submitted
	// the name of a folder) or gets a single file name (is user
	// has submitted only the file name)
	// ===================================================
	addFiles(new File(fileName));

	int originalNumDocs = writer.numDocs();
	for (File f : queue) {
	    FileReader fr = null;
	    try {
		Document doc = new Document();

		// ===================================================
		// add contents of file
		// ===================================================
		fr = new FileReader(f);
		doc.add(new TextField("contents", fr));
		doc.add(new StringField("path", f.getPath(), Field.Store.YES));
		doc.add(new StringField("filename", f.getName(),
			Field.Store.YES));

		writer.addDocument(doc);
		System.out.println("Added: " + f);
	    } catch (Exception e) {
		System.out.println("Could not add: " + f);
	    } finally {
		fr.close();
	    }
	}

	int newNumDocs = writer.numDocs();
	System.out.println("");
	System.out.println("************************");
	System.out
		.println((newNumDocs - originalNumDocs) + " documents added.");
	System.out.println("************************");

	queue.clear();
    }

    private void addFiles(File file) {

	if (!file.exists()) {
	    System.out.println(file + " does not exist.");
	}
	if (file.isDirectory()) {
	    for (File f : file.listFiles()) {
		addFiles(f);
	    }
	} else {
	    String filename = file.getName().toLowerCase();
	    // ===================================================
	    // Only index text files
	    // ===================================================
	    if (filename.endsWith(".htm") || filename.endsWith(".html")
		    || filename.endsWith(".xml") || filename.endsWith(".txt")) {
		queue.add(file);
	    } else {
		System.out.println("Skipped " + filename);
	    }
	}
    }

    /**
     * Close the index.
     * 
     * @throws java.io.IOException
     *             when exception closing
     */
    public void closeIndex() throws IOException {
	writer.close();
    }
    public static void writeExcelFile(ScoreDoc[] hits, IndexSearcher searcher, int qCount, String fileName){
    	HSSFWorkbook wb = new HSSFWorkbook();
    	HSSFSheet sheet = wb.createSheet("Query"+qCount);
    	 int rowCount = 0;
    	
 		for (int i = 1; i <= hits.length; ++i) 
 		{
 			Row row = sheet.createRow(i-1);
 			int docId = hits[i-1].doc; 
 			Document d;
 			String name="";
			try {
				d = searcher.doc(docId);
				int  lastindex = d.get("path").lastIndexOf("\\");
    			String fName = d.get("path").substring(lastindex+1);
    			name = fName;
			} catch (IOException e) 
			{
				
				e.printStackTrace();
			}
			
            int columnCount = 0;
            row.createCell(0).setCellValue((Integer) qCount);
            row.createCell(1).setCellValue((String) "Q0");
            row.createCell(2).setCellValue((String) name);
            row.createCell(3).setCellValue((Integer) i);
            row.createCell(4).setCellValue((Float) hits[i-1].score);
            row.createCell(5).setCellValue((String) "lucene-sys");
 			
            
          
 		}
 		try (FileOutputStream outputStream = new FileOutputStream("lucenefiles"+File.separator+"LuceneCACM"+qCount+".xls")) {
 	        wb.write(outputStream);
 	    } catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
 		
 		
    }
    public static void displayResults(ScoreDoc[] hits, IndexSearcher searcher, int qCount, String fileName){
    	HashMap<Integer,String> mapping = new HashMap<Integer,String>();
    	try {
    		FileWriter fw,fw1;

			fw = new FileWriter(fileName+"Int.txt");
			fw1 = new FileWriter(fileName+".txt");
			String newLine = System.getProperty("line.separator");
			String formatDouble = "%-8d %-2s %-6d %-5d %-8.6f %-15s%n";
			String formatDouble1 = "%-8d %-2s %-50s %-5d %-8.6f %-15s%n";
			
			String formatStr = "%-8s %-2s %-6s %-5s %-8s %-15s%n";
			String formatStr1 = "%-8s %-2s %-50s %-5s %-8s %-15s%n";
			
			fw.write(String.format(formatStr, "Query_Id", "Q0", "Doc_Id","Rank","Score","System_Name"));
			
			fw1.write(String.format(formatStr1, "Query_Id", "Q0", "Doc_Id","Rank","Score","System_Name"));
			
    		
    		
    	
    		for (int i = 0; i < hits.length; ++i) {
    			int docId = hits[i].doc; 
    			Document d;
    			d = searcher.doc(docId);
    			fw.write(String.format(formatDouble, qCount,"Q0",docId, (i+1),hits[i].score,"Lucene-System"));
    			
    			int  lastindex = d.get("path").lastIndexOf("\\");
    			String fName = d.get("path").substring(lastindex+1);
    			mapping.put(docId, fName);
    			fw1.write(String.format(formatDouble1, qCount,"Q0",fName, (i+1),hits[i].score,"Lucene-System"));
    			
    		}
    		fw.close();
    		fw1.close();

			fw = new FileWriter("mapping.txt");
			formatDouble = "%-8d %-25s%n";
			formatStr = "%-8s %-25s%n";
			fw.write(String.format(formatStr, "DOC-ID", "FILE-NAME"));
			
			for(int docID : mapping.keySet())
			{ 
				fw.write(String.format(formatDouble, docID,mapping.get(docID)));
			}
			fw.close();
    		
    		
    	} catch (IOException e) {
    		// TODO Auto-generated catch block
    		e.printStackTrace();
    	}
    	
    	
    }
    
    private static HashMap<String, Integer> populateWordFrequency(IndexReader reader, TermsEnum j,
			int count, HashMap<String, Integer> wordFrequency) throws IOException {
		BytesRef byteReference;
		while((byteReference= j.next()) != null)
		{
			String singleTerm=new String(byteReference.bytes, byteReference.offset, byteReference.length);
			Term termObject = new Term("contents",singleTerm); 
			int termFrequency = (int) reader.totalTermFreq(termObject);
			totalFrequency += termFrequency;
			wordFrequency.put(singleTerm, termFrequency);
			count++;
		}
		return wordFrequency;
    }
    
    
    private static LinkedHashMap<String, Integer> sortWordFrequency(HashMap<String, Integer> unsortMap, final boolean order) {
        

		 List<Entry<String, Integer>> list = new LinkedList<Entry<String, Integer>> (unsortMap.entrySet());

		
		 Collections.sort(list, new Comparator<Entry<String, Integer>>()
		 {
			 public int compare(Entry<String, Integer> o1,
					 Entry<String, Integer> o2)
			 {
				 if (order) 
				 {
					 return o1.getValue().compareTo(o2.getValue());
				 }
				 else
				 {
					 return o2.getValue().compareTo(o1.getValue());

				 }
			 }
		 });

		
		 LinkedHashMap<String, Integer> sortedMap = new LinkedHashMap<String, Integer>();
		 for (Entry<String, Integer> entry : list)
		 {
			 sortedMap.put(entry.getKey(), entry.getValue());
		 }

		 return sortedMap;
	 }

    
   
    
}