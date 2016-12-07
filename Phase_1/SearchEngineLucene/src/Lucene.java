
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;

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
import org.jsoup.Jsoup;
/**
 * To create Apache Lucene index in a folder and add files into this index based
 * on the input of the user.
 */
public class Lucene {
	//    private static Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_47);
	private static Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_47);
    private static Analyzer sAnalyzer = new SimpleAnalyzer(Version.LUCENE_47);


	private IndexWriter writer;
	private ArrayList<File> queue = new ArrayList<File>();

	public static void main(String[] args) throws IOException {
		System.out
		.println("Enter the FULL path where the index will be created: (e.g. /Usr/index or c:\\temp\\index)");

		String indexLocation = null;
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		String s = br.readLine();

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
		// fetch unique terms and term frequency
		// =========================================================
		IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(
				indexLocation)));

		Fields fields = MultiFields.getFields(reader);
		Terms terms = fields.terms("contents");
		TermsEnum iterator = terms.iterator(null);
		BytesRef byteRef = null;
		Set<String> uniqueTerms = new HashSet<String>();
		HashMap<String, Long> term_and_freq = new HashMap<String, Long>();


		while((byteRef = iterator.next()) != null) {
			String term = new String(byteRef.bytes, byteRef.offset, byteRef.length); 
			uniqueTerms.add(term);
			Term termInstance = new Term("contents", term);
			long termFreq = reader.totalTermFreq(termInstance);
			term_and_freq.put(term, termFreq);
			System.out.println(term + "->" + termFreq);	 
		}

		// printing total unique terms in the corpus
		System.out.println(uniqueTerms.size());  

		// sorting (unique_term , frequency) pair based on descending order of frequency.
		SortMap smo = new SortMap();
		term_and_freq = smo.sortHashMap(term_and_freq);

		// Writing sorted (unique_term, frequency) pair to text file.
		WritePair wh = new WritePair();
		wh.writeToFile(term_and_freq);    

		// =========================================================
		// query search
		// =========================================================
		IndexSearcher searcher = new IndexSearcher(reader);		

		// List of given queries to be searched.
		String queries[] = 
				/* "portable operating systems",
				"code optimization for space efficiency",
				"parallel algorithms",
				"distributed computing structure and algorithms", 
				"applied stochast process", 
				"perform evaluation and model of computer system", 
				"parallel processor in information retrieval"}; */
				
				{"portabl oper system", 
				"code optim for space effici",
				"parallel algorithm", 
				"distribut comput structur and algorithm", 
				"appli stochast process", 
				"perform evalu and model of comput system", 
				"parallel processor in inform retriev"}; 


		

		try{
			File file = new File("/Users/meghnatulasi/Desktop/IRProject\top100.txt");

			// if file doesn't exists, then create it
			if (!file.exists()) {
				file.createNewFile();
			}

			FileWriter fw = new FileWriter(file.getAbsoluteFile());
			BufferedWriter bw = new BufferedWriter(fw);

			for(int z = 0;z<queries.length ;z++)
			{
				try
				{
					s = queries[z];
					TopScoreDocCollector collector = TopScoreDocCollector.create(100, true);
					Query q = new QueryParser(Version.LUCENE_47, "contents", sAnalyzer).parse(s);
					searcher.search(q, collector);
					ScoreDoc[] hits = collector.topDocs().scoreDocs;

					// 4. display results		
					System.out.println("Found " + hits.length + " hits.");
					for (int i = 0; i < hits.length; ++i) {
						int docId = hits[i].doc;
						Document d = searcher.doc(docId);
						String line = "Query : " + s + " Rank : " + (i + 1) + " File : " + d.get("filename")
								+ " score : " + hits[i].score + "\n";
						System.out.println(line);
						bw.write(line);
					}
					// 5. term stats --> watch out for which "version" of the term
					// must be checked here instead!
					Term termInstance = new Term("contents", s);
					long termFreq = reader.totalTermFreq(termInstance);
					long docCount = reader.docFreq(termInstance);
					System.out.println(s + " Term Frequency " + termFreq
							+ " - Document Frequency " + docCount);

				} 
				catch (Exception e) {
					System.out.println("Error searching " + s + " : " + e.getMessage());
					break;
				}
				bw.write("================================================================ \n");
			}
			bw.close();
		}
		catch(Exception e)
		{System.out.println("Error in File Handling : " + e.getMessage());}
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

		IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47, sAnalyzer);

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
			try {
				Document doc = new Document();

				// parsing html documents using Jsoup to avoid html tags
				org.jsoup.nodes.Document doc1 = Jsoup.parse(f, "UTF-8", "");
				String body = doc1.body().text();
				StringReader str = new StringReader(body);

				// ===================================================
				// add contents of file
				// ===================================================
				doc.add(new TextField("contents", str));
				doc.add(new StringField("path", f.getPath(), Field.Store.YES));
				doc.add(new StringField("filename", f.getName(),
						Field.Store.YES));

				writer.addDocument(doc);
				System.out.println("Added: " + f);
			} catch (Exception e) {
				System.out.println("Could not add: " + f);
			} finally {
				//fr.close();
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

}