import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Set;


public class WritePair {

	 public void writeToFile(HashMap<String,Long> term_and_freq) throws IOException
	    {	    	
	    	Set keySet = term_and_freq.keySet();
	    	System.out.println("Writing Term-Frequency pair to text file");
			 Iterator i = keySet.iterator();
			 PrintWriter pw = new PrintWriter(new FileWriter("/Users/meghnatulasi/Documents/IR/SearchEngineLucene/sortedtermlist.txt",true));
			 			 
			 Integer line_count = 1;
			 while (i.hasNext()) {
				
				 String rank = line_count.toString();
				 String line = rank + "|";
				 
				 String term = (String) i.next();
				 line = line + term + "|" + term_and_freq.get(term).toString() + "\n";
				 pw.write(line);
				 line_count++; }
			pw.close(); } }