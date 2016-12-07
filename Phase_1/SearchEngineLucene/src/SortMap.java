import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

public class SortMap{
	
	public  HashMap<String,Long> sortHashMap(HashMap<String,Long> term_freq )
	{
		List<Map.Entry<String,Long>> linkedList = new LinkedList<Map.Entry<String,Long>>(term_freq.entrySet());
		linkedList = callComparator(linkedList);
		Map<String,Long> sortedHashMap = new LinkedHashMap<String,Long>();
		for (Iterator<Map.Entry<String,Long>> i = linkedList.iterator(); i.hasNext();)
		{
			Map.Entry<String,Long> pair = i.next();
			sortedHashMap.put(pair.getKey(), pair.getValue());
		}
		return (HashMap<String,Long>) sortedHashMap;
	}
	private List<Entry<String, Long>> callComparator(List<Entry<String, Long>> linkedList) {
		
		Collections.sort(linkedList , new Comparator<Map.Entry<String,Long>>()
		{
			public int  compare (Map.Entry<String,Long> entry1 ,Map.Entry<String,Long> entry2)
			{
				return(entry2.getValue()).compareTo(entry1.getValue());
			}});
		return linkedList; }}