package algorithms.RASP;

import tools.MemoryLogger;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.text.SimpleDateFormat;
import java.util.*;
import java.util.Map.Entry;

public class RASP_Case {
	/** the current level k in the breadth-first search */
	int k;

	/** variables for counting support of items */
	Map<Integer, BitSet> mapItemTIDs;
	Map<Integer, BitSet> mapHeaderTIDs;
	int mapItemTIDsSize;

	/** the number of transactions */
	int widcount = 0;
	int sumCount = 0;

	int[] minsup;

	/** total number of candidates */
	int maxCandidate = 0;
	int maxCandidateK = 0;
	int frequentCount = 0;
	int frequent_1Count = 0;

	/** number of candidates generated during last execution */
	long elapsedTimestamp = 0;
	long startTimestamp;
	long kTimestamp;
	long timestamp;

	FPNode_Real root;

	/** object to write the output file (if the user wants to write to a file) */
	BufferedWriter writerOutput = null;

	/** maximum pattern length */
	int maxPatternLength;

	String filePath;
	/** window length */
	int denom;
	int recordingTime;
	int binSize;
	int interLen;
	int winLen;
	int rangeBins;
	int maxItem;

	List<Integer> prefixList;
	int prefixSize;

	List<FPNode_Real> prefixNodeList;
	int prefixNodeSize;
	
	/**
	 * Default constructor
	 */
	public RASP_Case() {

	}

	/**
	 * Method to run the algorithm
	 * @throws IOException exception if error while writting or reading the input/output file
	 */
	public void runAlgorithm(String filePath, int time, int maxitem, int length, int binsize, int winLen, int interLen, int rangeBins, long timestamp) throws IOException {
		// record the start time
		startTimestamp = System.currentTimeMillis();

		this.filePath = filePath;
		this.recordingTime = time;
		this.maxItem = maxitem;
		this.maxPatternLength = length;
		this.binSize = binsize;
		this.winLen = winLen;
		this.interLen = interLen;
		this.denom = recordingTime;
		this.rangeBins = rangeBins;

		String input = String.format("./txt/datasets/ecommerce/%s_time_%d_item_%d_bin_%d_winlen_%d.txt", filePath, time, maxitem, binsize, winLen);
		Files.createDirectories(Paths.get(String.format("./TSPs/%s_RASP_1", filePath)));
		String output = String.format("./TSPs/%s_RASP_1/%s_time_%d_item_%d_length_%d_bin_%d_winlen_%d_interlen_%d_rangebins_%d", filePath, filePath, time, maxitem, length, binsize, winLen, interLen, rangeBins);

		// reset the utility for checking the memory usage
		MemoryLogger.getInstance().reset();

		maxItem = 1;

		this.timestamp = timestamp;

		// initialize variable to count the number of transactions
		widcount = 0;

		// read the input file line by line until the end of the file
		// (each line is a transaction)
		mapItemTIDs = new LinkedHashMap<>();
		mapHeaderTIDs = new LinkedHashMap<>();
		// key : item   value: widset of the item as a bitset

		// scan the database to load it into memory and count the support of each single item at the same time
		BufferedReader reader = new BufferedReader(new FileReader(input));
		String line;
		String[] lineSplited;
		int lineSplitedLength;
		Integer item;
		int itemItem;
		int itemBin;
		sumCount = 0;
		// for each line (transactions) until the end of the file
		while (((line = reader.readLine()) != null)) {
			// if the line is  a comment, is  empty or is a
			// kind of metadata
			if (line.isEmpty() || line.charAt(0) == '#' || line.charAt(0) == '%' || line.charAt(0) == '@') {
				continue;
			}
			// split the line according to spaces
			lineSplited = line.split(" ");
			lineSplitedLength = lineSplited.length;
			BitSet wids;
			// for each item in this line (transaction)
			for (int i=0; i< lineSplitedLength; i++) {
				// transform this item from a string to an integer
				item = Integer.parseInt(lineSplited[i]);
				itemItem = item / winLen;
				itemBin = item % winLen;
				// increase the support count
				if (itemBin == 0) {
					// update the widset of the item
					wids = mapHeaderTIDs.get(item);
					if (wids == null) {
						wids = new BitSet();
						mapHeaderTIDs.put(item, wids);
					}
					wids.set(widcount);
					if (itemItem + 1 > maxItem) {
						maxItem = itemItem + 1;
					}
					sumCount += 1;
				}
				// update the widset of the item
				item = itemItem * winLen + itemBin / rangeBins * rangeBins;
				wids = mapItemTIDs.get(item);
				if (wids == null) {
					wids = new BitSet();
					mapItemTIDs.put(item, wids);
				}
				wids.set(widcount);
			}
			// increase the transaction count
			widcount++;
		}
		// close the input file
		reader.close();

		root = new FPNode_Real();
		minsup = new int[maxPatternLength - 1];
		minsup[0] = (int) Math.max(Math.round(denom * Math.pow((double) sumCount / maxItem / denom, 2) * 2 * 0.5), 2);

		// We sort the list of candidates by lexical order
		// (Apriori need to use a total order otherwise it does not work)
		mapItemTIDs = sortMapByKey(mapItemTIDs);
		mapHeaderTIDs = sortMapByKey(mapHeaderTIDs);

		// For each item
		for (Entry<Integer, BitSet> entry : mapHeaderTIDs.entrySet()) {
			// for the current item
			// get the support count (cardinality of the widset)
			// add the sorted transaction to the fptree.
			// there is no node, we create a new one
			FPNode_Real nextNode = new FPNode_Real();
			nextNode.itemID = entry.getKey();
			BitSet wids = entry.getValue();
			nextNode.wids = wids;
			nextNode.counter = wids.cardinality();
			// we link the new node to its parent
			root.addChild(nextNode);
		}
		mapItemTIDsSize = mapItemTIDs.size();
		frequentCount = mapHeaderTIDs.size() + mapItemTIDsSize;
		mapHeaderTIDs = null;
		maxCandidate = (int) Math.round(1e+9 / widcount);

		for (k = 2; k <= maxPatternLength; k++) {
			runK(output);
		}

		// record end time
		elapsedTimestamp = System.currentTimeMillis() - startTimestamp;
		MemoryLogger.getInstance().checkMemory();
		
		BufferedWriter writerTime = new BufferedWriter(new FileWriter(String.format("./txt/datasets/ecommerce/time_RASP/%s_time_%d_item_%d_length_%d_bin_%d_winlen_%d_interlen_%d_rangebins_%d_%s.csv", filePath, time, maxitem, length, binsize, winLen, interLen, rangeBins, new SimpleDateFormat( "MM.dd_HH.mm").format(timestamp)), true));
		writerTime.write(String.format("%s,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d", filePath, time, maxitem, length, binsize, winLen, interLen, rangeBins, minsup[k - 3], k - 1, frequentCount, elapsedTimestamp));
		writerTime.newLine();
		writerTime.close();

		// close the output file if the result was saved to a file.
		if(writerOutput != null){
			writerOutput.close();
		}
	}

	// We sort the list of candidates by lexical order
	// (Apriori need to use a total order otherwise it does not work)
	LinkedHashMap<Integer, BitSet> sortMapByKey(Map<Integer, BitSet> map) {
		List<Entry<Integer, BitSet>> entries = new LinkedList<>(map.entrySet());
		Collections.sort(entries, new Comparator<Entry<Integer, BitSet>>() {
			public int compare(Entry<Integer, BitSet> e1, Entry<Integer, BitSet> e2) {
				int o1 = e1.getKey();
				int o2 = e2.getKey();
				int c = o1 % winLen - o2 % winLen;
				if (c == 0) {
					c = o1 / winLen - o2 / winLen;
				}
				return c;
			}
		});
		LinkedHashMap<Integer, BitSet> result = new LinkedHashMap<>();
		for (Entry<Integer, BitSet> entry : entries) {
			result.put(entry.getKey(), entry.getValue());
		}
		return result;
	}

	/**
	 * Method to run the algorithm
	 * @throws IOException exception if error while writting or reading the input/output file
	 */
	public void runK(String output) throws IOException {
		// we add the number of candidates generated to the total
		frequent_1Count = frequentCount;
		frequentCount = 0;
		if (k < maxPatternLength - 1) {
			maxCandidateK = (maxCandidate - mapItemTIDsSize) / 2;
		} else if (k == maxPatternLength) {
			maxCandidateK = maxCandidate - mapItemTIDsSize - frequent_1Count;
		}
		kTimestamp = System.currentTimeMillis();
		// we check the memory usage
		MemoryLogger.getInstance().checkMemory();

		// close the output file if the result was saved to a file.
		if (writerOutput != null) {
			writerOutput.close();
		}
		writerOutput = new BufferedWriter(new FileWriter(output + String.format("_%d.txt", k)));

		// if we are at level k=2, we use an optimization to generate candidates
		if (k == 2) {
			generateCandidate2();
		}
		// otherwise we use the regular way to generate candidates
		else {
			minsup[k - 2] = (int) Math.max(Math.round(denom * Math.pow((double) sumCount / maxItem / denom, k) * Math.pow(2, k - 1) * 0.5), Math.max(Math.round((double) sumCount / maxItem * 0.005), 2));
			if (k == 3) {
				for (FPNode_Real rootChild : root.childs) {
					// for the current item
					prefixList = new ArrayList<>();
					prefixSize = 0;
					generateCandidate3(rootChild);
				}
			}
			else {
				for (FPNode_Real rootChild : root.childs) {
					// for the current item
					prefixList = new ArrayList<>();
					prefixSize = 0;
					generateCandidateK(rootChild, 0, rootChild);
				}
			}
		}
		if (k < maxPatternLength) {
			List<FPNode_Real> rootChilds = root.childs;
			int rootChildsSize = rootChilds.size();
			for (int iChild = 0; iChild < rootChildsSize; iChild++) {
				// for the current item
				prefixNodeList = new ArrayList<>();
				prefixNodeSize = 0;
				cleanCandidates(rootChilds.get(iChild + rootChilds.size() - rootChildsSize), k);
			}
		}
		System.out.printf("%s_time_%d_item_%d_length_%d_bin_%d_winlen_%d_interlen_%d_rangebins_%d_sup_%d_k_%d_freq_%d_time_%d\n", filePath, recordingTime, maxItem, maxPatternLength, binSize, winLen, interLen, rangeBins, minsup[k - 2], k, frequentCount, System.currentTimeMillis() - kTimestamp);
	}

	/**
	 * This method generates candidates itemsets of size 2 based on
	 * itemsets of size 1.
	 */
	void generateCandidate2() throws IOException {
		int item1Item;
		// For each itemset I1 and I2 of level k-1
		for (FPNode_Real item1Node : root.childs) {
			// for the current item
			item1Item = item1Node.itemID / winLen;
			for (int item2Item = 0; item2Item < maxItem; item2Item++) {
				if (item1Item == item2Item) {
					continue;
				}
				int item2 = item2Item * winLen;
				BitSet item2TIDs = mapItemTIDs.get(item2);
				if (item2TIDs != null) {
					item2TIDs = (BitSet) item2TIDs.clone();
					item2TIDs.and(item1Node.wids);
					int item2NodeCounter = item2TIDs.cardinality();
					if (item2NodeCounter >= minsup[k - 2] && (saveCandidate() || item2NodeCounter >= minsup[k - 2])) {
						FPNode_Real item2Node = new FPNode_Real();
						item2Node.itemID = item2;
						item2Node.wids = item2TIDs;
						item2Node.counter = item2NodeCounter;
						item1Node.addChild(item2Node);
					}
				}
			}
			for (int item2Bin = this.rangeBins; item2Bin <= interLen; item2Bin = (item2Bin + rangeBins)) {
				for (int item2Item = 0; item2Item < maxItem; item2Item++) {
					if (item1Item == item2Item) {
						continue;
					}
					int item2 = item2Item * winLen + item2Bin;
					BitSet item2TIDs = mapItemTIDs.get(item2);
					BitSet item2TIDsRange = mapItemTIDs.get(item2 - rangeBins);
					if (item2TIDs != null || item2TIDsRange != null) {
						if (item2TIDs != null) {
							item2TIDs = (BitSet) item2TIDs.clone();
							if (item2TIDsRange != null) {
								item2TIDs.or(item2TIDsRange);
							}
						} else {
							item2TIDs = (BitSet) item2TIDsRange.clone();
						}
						item2TIDs.and(item1Node.wids);
						int item2NodeCounter = item2TIDs.cardinality();
						if (item2NodeCounter >= minsup[k - 2] && (saveCandidate() || item2NodeCounter >= minsup[k - 2])) {
							FPNode_Real item2Node = new FPNode_Real();
							item2Node.itemID = item2;
							item2Node.wids = item2TIDs;
							item2Node.counter = item2NodeCounter;
							item1Node.addChild(item2Node);
						}
					}
				}
			}
		}
	}

	/**
	 * Return the immediate child of this node having a given ID.
	 * If there is no such child, return null;
	 */
	FPNode_Real getChild (List<FPNode_Real> childs, int id) {
		int left = 0;
		int right = childs.size() - 1;

		while (left <= right) {
			int mid = left + (right - left) / 2;

			FPNode_Real midNode = childs.get(mid);
			int midId = midNode.itemID;
			int c = midId % winLen - id % winLen;
			if (c == 0) {
				c = midId / winLen - id / winLen;
			}

			if (c == 0) {
				return midNode; // Element found
			} else if (c < 0) {
				left = mid + 1;
			} else {
				right = mid - 1;
			}
		}
		return null; // Element not found
	}

	int getChildIndex (List<FPNode_Real> childs, int id) {
		int left = 0;
		int right = childs.size() - 1;

		while (left <= right) {
			int mid = left + (right - left) / 2;
			int midId = childs.get(mid).itemID;
			int c = midId % winLen - id % winLen;
			if (c == 0) {
				c = midId / winLen - id / winLen;
			}

			if (c == 0) {
				return mid; // Element found
			} else if (c < 0) {
				left = mid + 1;
			} else {
				right = mid - 1;
			}
		}
		return -1; // Element not found
	}

	public static long candidateIntToNeuronNumber(List<Integer> candidate, int maxItem, int k, int winLen) {
		long number = candidate.get(0) / winLen * (long) Math.pow(maxItem, k - 1);
		for (int i = 1; i < k; i++) {
			number += candidate.get(i) / winLen * (long) Math.pow(maxItem, k - i - 1);
		}
		return number;
	}

	public static long candidateIntToInterNumber(List<Integer> candidate, int maxItem, int k, int winLen) {
		long number = candidate.get(1) % winLen * (long) Math.pow(winLen, k - 2);
		for (int i = 2; i < k; i++) {
			number += candidate.get(i) % winLen * (long) Math.pow(winLen, k - i - 1);
		}
		return number;
	}

	void generateCandidate3(FPNode_Real node) throws IOException {
		prefixList.add(node.itemID);
		prefixSize++;
		if (prefixSize == 2) {
			int item2Bin = node.itemID % winLen;
			FPNode_Real item2Node = getChild(root.childs, node.itemID - item2Bin);
			if (item2Node != null) {
				for (FPNode_Real item3Node : item2Node.childs) {
					// for the current item
					if (prefixList.get(0) / winLen == item3Node.itemID / winLen) {
						continue;
					}
					int item3Bin = item3Node.itemID % winLen;
					if ((item2Bin + item3Bin) >= winLen) {
						break;
					}
					int item = item3Node.itemID + item2Bin;
					prefixList.add(item);
					prefixSize++;
					BitSet itemTIDs = mapItemTIDs.get(item);
					BitSet itemTIDsRange = null;
					if (item3Bin >= rangeBins) {
						itemTIDsRange = mapItemTIDs.get(item - rangeBins);
					}
					if ((itemTIDs != null || itemTIDsRange != null)) {
						if (itemTIDs != null) {
							itemTIDs = (BitSet) itemTIDs.clone();
							if (itemTIDsRange != null) {
								itemTIDs.or(itemTIDsRange);
							}
						} else {
							itemTIDs = (BitSet) itemTIDsRange.clone();
						}
						itemTIDs.and(node.wids);
						int nextNodeCounter = itemTIDs.cardinality();
						// if the result should be saved to a file
						writerOutput.write(candidateIntToNeuronNumber(prefixList, maxItem, 3, winLen) + " " + candidateIntToInterNumber(prefixList, maxItem, 3, winLen) + " " + nextNodeCounter);
						writerOutput.newLine();
						if (nextNodeCounter >= minsup[k - 2] && (saveCandidate() || nextNodeCounter >= minsup[k - 2])) {
							FPNode_Real nextNode = new FPNode_Real();
							nextNode.itemID = item;
							nextNode.wids = itemTIDs;
							nextNode.counter = nextNodeCounter;
							node.addChild(nextNode);
						}
					}
					prefixList.remove(prefixSize - 1);
					prefixSize--;
				}
			}
			prefixList.remove(prefixSize - 1);
			prefixSize--;
		}
		else {
			List<FPNode_Real> nodeChilds = node.childs;
			int nodeChildsSize = nodeChilds.size();
			for (int iChild = 0; iChild < nodeChildsSize; iChild++) {
				generateCandidate3(nodeChilds.get(iChild + nodeChilds.size() - nodeChildsSize));
			}
			prefixList.remove(prefixSize - 1);
			prefixSize--;
		}
	}

	void generateCandidateK(FPNode_Real node, int item2BinInput, FPNode_Real item2NodeInput) throws IOException {
		prefixList.add(node.itemID);
		prefixSize++;
		if (prefixSize == k - 1) {
			for (FPNode_Real itemLastNode : item2NodeInput.childs) {
				// for the current item
				if (prefixList.get(0) / winLen == itemLastNode.itemID / winLen) {
					continue;
				}
				int itemLastBin = itemLastNode.itemID % winLen;
				if ((item2BinInput + itemLastBin) >= winLen) {
					break;
				}
				int item = itemLastNode.itemID + item2BinInput;
				prefixList.add(item);
				prefixSize++;
				BitSet itemTIDs = mapItemTIDs.get(item);
				BitSet itemTIDsRange = null;
				if (itemLastBin - item2NodeInput.itemID % winLen >= rangeBins) {
					itemTIDsRange = mapItemTIDs.get(item - rangeBins);
				}
				if ((itemTIDs != null || itemTIDsRange != null)) {
					if (itemTIDs != null) {
						itemTIDs = (BitSet) itemTIDs.clone();
						if (itemTIDsRange != null) {
							itemTIDs.or(itemTIDsRange);
						}
					} else {
						itemTIDs = (BitSet) itemTIDsRange.clone();
					}
					itemTIDs.and(node.wids);
					int nextNodeCounter = itemTIDs.cardinality();
					writerOutput.newLine();
					if (nextNodeCounter >= minsup[k - 2] && (saveCandidate() || nextNodeCounter >= minsup[k - 2])) {
						FPNode_Real nextNode = new FPNode_Real();
						nextNode.itemID = item;
						nextNode.wids = itemTIDs;
						nextNode.counter = nextNodeCounter;
						node.addChild(nextNode);
						// if the result should be saved to a file
						writerOutput.write(candidateIntToNeuronNumber(prefixList, maxItem, k, winLen) + " " + candidateIntToInterNumber(prefixList, maxItem, k, winLen) + " " + nextNodeCounter);
					}
				}
				prefixList.remove(prefixSize - 1);
				prefixSize--;
			}
			prefixList.remove(prefixSize - 1);
			prefixSize--;
		}
		else {
			for (FPNode_Real nextNode: node.childs) {
				FPNode_Real item2Node;
				if (prefixSize > 1) {
					item2Node = getChild(item2NodeInput.childs, nextNode.itemID - item2BinInput);
				} else {
					item2BinInput = nextNode.itemID % winLen;
					item2Node = getChild(root.childs, nextNode.itemID - item2BinInput);
				}
				if (item2Node != null) {
					generateCandidateK(nextNode, item2BinInput, item2Node);
				}
			}
			prefixList.remove(prefixSize - 1);
			prefixSize--;
		}
	}

	boolean saveCandidate() throws IOException {
		frequentCount++;
		if (frequentCount > maxCandidateK) {
			System.out.printf("%s_time_%d_item_%d_length_%d_bin_%d_winlen_%d_interlen_%d_rangebins_%d_sup_%d_k_%d", filePath, recordingTime, maxItem, maxPatternLength, binSize, winLen, interLen, rangeBins, minsup[k - 2], k);
			minsup[k - 2] += 1;
			for (FPNode_Real rootChild : root.childs) {
				// for the current item
				prefixNodeList = new ArrayList<>();
				prefixNodeSize = 0;
				pruneCandidates(rootChild, k, root.childs);
			}
			System.out.printf("_freq_%d_time_%d\n", frequentCount, System.currentTimeMillis() - kTimestamp);
			return false;
		}
		return true;
	}

	void pruneCandidates(FPNode_Real node, int kPrune, List<FPNode_Real> parentNodeChilds) throws IOException {
		prefixNodeSize++;
		if (prefixNodeSize == kPrune) {
			if (node.counter < minsup[k - 2]) {
				node.wids = null;
				parentNodeChilds.remove(getChildIndex(parentNodeChilds, node.itemID));
				frequentCount--;
			}
			prefixNodeSize--;
		}
		else {
			List<FPNode_Real> nodeChilds = node.childs;
			if (nodeChilds != null) {
				int nodeChildsSize = nodeChilds.size();
				for (int iChild = 0; iChild < nodeChildsSize; iChild++) {
					// for the current item
					pruneCandidates(nodeChilds.get(iChild + nodeChilds.size() - nodeChildsSize), kPrune, nodeChilds);
				}
			}
			prefixNodeSize--;
		}
	}

	void cleanCandidates(FPNode_Real node, int kPrune) {
		prefixNodeList.add(node);
		prefixNodeSize++;
		if (prefixNodeSize == kPrune - 1) {
			node.wids = null;
			if (node.childs == null || node.childs.isEmpty()) {
				List<FPNode_Real> parentChilds;
				if (prefixNodeSize > 1) {
					parentChilds = prefixNodeList.get(prefixNodeSize - 2).childs;
				} else {
					parentChilds = root.childs;
				}
				parentChilds.remove(getChildIndex(parentChilds, node.itemID));
				if (parentChilds.isEmpty()) {
					for (int iChild = prefixNodeSize - 3; iChild >= 0; iChild--) {
						parentChilds = prefixNodeList.get(iChild).childs;
						FPNode_Real childNode = prefixNodeList.get(iChild + 1);
						childNode.wids = null;
						parentChilds.remove(getChildIndex(parentChilds, childNode.itemID));
						if (!parentChilds.isEmpty()) {
							break;
						}
					}
				}
			}
			prefixNodeList.remove(prefixNodeSize - 1);
			prefixNodeSize--;
		}
		else {
			List<FPNode_Real> nodeChilds = node.childs;
			int nodeChildsSize = nodeChilds.size();
			for (int iChild = 0; iChild < nodeChildsSize; iChild++) {
				// for the current item
				cleanCandidates(nodeChilds.get(iChild + nodeChilds.size() - nodeChildsSize), kPrune);
			}
			prefixNodeList.remove(prefixNodeSize - 1);
			prefixNodeSize--;
		}
	}

	/**
	 * Print statistics about the algorithm execution to System.out.
	 */
	public void printStats() {
		System.out.println("=============  APRIORI - STATS =============");
		System.out.println(" Maximum memory usage : " + MemoryLogger.getInstance().getMaxMemory() + " mb");
		System.out.println(" Total time ~ " + elapsedTimestamp + " ms");
		System.out.println("===================================================");
	}
}
