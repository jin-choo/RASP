package algorithms.RASP;

import tools.MemoryLogger;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.text.SimpleDateFormat;
import java.util.*;
import java.util.Map.Entry;

public class RASP_O {
	/** the current level k in the breadth-first search */
	int k;

	/** variables for counting support of items */
	Map<Short, BitSet> mapItemTIDs;
	Map<Short, BitSet> mapHeaderTIDs;
	int mapItemTIDsSize;

	/** the number of transactions */
	int widcount = 0;

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

	FPNode root;

	/** object to write the output file (if the user wants to write to a file) */
	BufferedWriter writerOutput = null;

	/** maximum pattern length */
	int maxPatternLength;

	int motifType;
	/** window length */
	int recordingTime;
	double backgroundFiringRate;
	double motifFiringRate;
	int binSize;
	int interLen;
	int winLen;
	int rangeBins;
	int maxItem;
	int seed;
	double pp;
	int temporalJitter;

	Map<Long, Integer> mapNeuronsMaxSup;

	List<Short> prefixList;
	int prefixSize;

	List<FPNode> prefixNodeList;
	int prefixNodeSize;

	/**
	 * Default constructor
	 */
	public RASP_O() {

	}

	/**
	 * Method to run the algorithm
	 * @throws IOException exception if error while writting or reading the input/output file
	 */
	public void runAlgorithm(int motifType, Integer NIDs, Integer recordingTime, double backgroundFiringRate, double pp, Integer temporalJitter, Integer timeWarping, double motifFiringRate, int motifNeurons, int motifNumbers, int motifMaxLags, int motifMaxSpikes, Integer binSize, Integer winLen, Integer rangeBins, long timestamp, int seed) throws IOException {
		// record the start time
		startTimestamp = System.currentTimeMillis();

		this.recordingTime = recordingTime;
		this.backgroundFiringRate = backgroundFiringRate;
		this.maxPatternLength = motifNeurons;
		this.motifFiringRate = motifFiringRate;
		this.binSize = binSize;
		this.motifType = motifType;
		if (motifType > 1) {
			this.interLen = (int) Math.ceil((double) motifMaxLags / binSize);
		} else {
			this.interLen = winLen;
		}
		this.winLen = winLen;
		this.rangeBins = rangeBins;
		this.seed = seed;
		this.pp = pp;
		this.temporalJitter = temporalJitter;

		String input = String.format("./txt/%d/%d_NIDs_%d_time_%d_bg_%.2f_pp_%.1f_tj_%d_tw_%d_mt_%.2f_%d_%d_%d_%d_bin_%d_winlen_%d_seed_%d.txt", motifType, motifType, NIDs, recordingTime, backgroundFiringRate, pp, temporalJitter, timeWarping, motifFiringRate, motifNeurons, motifNumbers, motifMaxLags, motifMaxSpikes, binSize, winLen, seed);
		Files.createDirectories(Paths.get(String.format("./TSPs/%d_RASP_o_1", motifType)));
		String output = String.format("./TSPs/%d_RASP_o_1/%d_RASP_o_NIDs_%d_time_%d_bg_%.2f_pp_%.1f_tj_%d_tw_%d_mt_%.2f_%d_%d_%d_%d_bin_%d_winlen_%d_interlen_%d_inter_%d_seed_%d", motifType, motifType, NIDs, recordingTime, backgroundFiringRate, pp, temporalJitter, timeWarping, motifFiringRate, motifNeurons, motifNumbers, motifMaxLags, motifMaxSpikes, binSize, winLen, interLen, rangeBins, seed);  // the path for saving the frequent itemsets found
		// reset the utility for checking the memory usage
		MemoryLogger.getInstance().reset();

		// READ THE INPUT FILE
		// Map to count the support of each item
		// Key: item  Value : support
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
		Short item;
		int itemItem;
		int itemBin;
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
				item = Short.parseShort(lineSplited[i]);
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
				}
				// update the widset of the item
				item = (short) (itemItem * winLen + itemBin / rangeBins * rangeBins);
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

		// convert the minimum support as a percentage to a
		// relative minimum support as an integer
		root = new FPNode();
		minsup = new int[maxPatternLength - 1];
		minsup[0] = 2;

		// We sort the list of candidates by lexical order
		// (Apriori need to use a total order otherwise it does not work)
		mapItemTIDs = sortMapByKey(mapItemTIDs);
		mapHeaderTIDs = sortMapByKey(mapHeaderTIDs);

		// For each item
		for (Entry<Short, BitSet> entry : mapHeaderTIDs.entrySet()) {
			// for the current item
			// get the support count (cardinality of the widset)
			// add the sorted transaction to the fptree.
			// there is no node, we create a new one
			FPNode nextNode = new FPNode();
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

		BufferedWriter writerTime = new BufferedWriter(new FileWriter(String.format("./txt/%d_RASP_o_time_%s.csv", motifType, new SimpleDateFormat( "MM.dd_HH.mm").format(timestamp)), true));
		writerTime.write(String.format("%d,%d,%d,%.2f,%.1f,%d,%d,%.2f,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d", motifType, NIDs, recordingTime, backgroundFiringRate, pp, temporalJitter, timeWarping, motifFiringRate, motifNeurons, motifNumbers, motifMaxLags, motifMaxSpikes, binSize, winLen, interLen, rangeBins, minsup[k - 3], k - 1, frequentCount, elapsedTimestamp, seed));
		writerTime.newLine();
		writerTime.close();

		// close the output file if the result was saved to a file.
		if(writerOutput != null){
			writerOutput.close();
		}
	}

	// We sort the list of candidates by lexical order
	// (Apriori need to use a total order otherwise it does not work)
	LinkedHashMap<Short, BitSet> sortMapByKey(Map<Short, BitSet> map) {
		List<Entry<Short, BitSet>> entries = new LinkedList<>(map.entrySet());
		Collections.sort(entries, new Comparator<Entry<Short, BitSet>>() {
			public int compare(Entry<Short, BitSet> e1, Entry<Short, BitSet> e2) {
				int o1 = e1.getKey();
				int o2 = e2.getKey();
				int c = o1 % winLen - o2 % winLen;
				if (c == 0) {
					c = o1 / winLen - o2 / winLen;
				}
				return c;
			}
		});
		LinkedHashMap<Short, BitSet> result = new LinkedHashMap<>();
		for (Entry<Short, BitSet> entry : entries) {
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
		} else if (k == maxPatternLength - 1) {
			maxCandidateK = maxCandidate - mapItemTIDsSize - 1000;
		} else if (k == maxPatternLength) {
			maxCandidateK = 1000;
		}
		kTimestamp = System.currentTimeMillis();
		// we check the memory usage
		MemoryLogger.getInstance().checkMemory();
		mapNeuronsMaxSup = new HashMap<>();

		// if we are at level k=2, we use an optimization to generate candidates
		if (k == 2) {
			generateCandidate2();
		}
		// otherwise we use the regular way to generate candidates
		else {
			minsup[k - 2] = 2;
			if (k == 3) {
				for (FPNode rootChild : root.childs) {
					// for the current item
					prefixList = new ArrayList<>();
					prefixSize = 0;
					generateCandidate3(rootChild);
				}
			}
			else {
				for (FPNode rootChild : root.childs) {
					// for the current item
					prefixList = new ArrayList<>();
					prefixSize = 0;
					generateCandidateK(rootChild, 0, rootChild);
				}
			}
		}
		if (k < maxPatternLength) {
			List<FPNode> rootChilds = root.childs;
			int rootChildsSize = rootChilds.size();
			for (int iChild = 0; iChild < rootChildsSize; iChild++) {
				// for the current item
				prefixNodeList = new ArrayList<>();
				prefixNodeSize = 0;
				cleanCandidates(rootChilds.get(iChild + rootChilds.size() - rootChildsSize), k);
			}
		}
		System.out.printf("%d_%d_bg_%.2f_mt_%.2f_pp_%.1f_tj_%d_bin_%d_win_%d_inter_%d_range_%d_sup_%d_k_%d_freq_%d_time_%d_seed_%d\n", motifType, recordingTime, backgroundFiringRate, motifFiringRate, pp, temporalJitter, binSize, this.winLen, this.interLen, rangeBins, minsup[k - 2], k, frequentCount, System.currentTimeMillis() - kTimestamp, seed);
		// close the output file if the result was saved to a file.
		if (writerOutput != null) {
			writerOutput.close();
		}
		writerOutput = new BufferedWriter(new FileWriter(output + String.format("_%d.txt", k)));
		for (Entry<Long, Integer> entry : mapNeuronsMaxSup.entrySet()) {
			// if the result should be saved to a file
			writerOutput.write(entry.getKey() + " " + entry.getValue());
			writerOutput.newLine();
		}
//		}
	}
	/**
	 * This method generates candidates itemsets of size 2 based on
	 * itemsets of size 1.
	 */
	void generateCandidate2() throws IOException {
		int item1Item;
		// For each itemset I1 and I2 of level k-1
		for (FPNode item1Node : root.childs) {
			// for the current item
			item1Item = item1Node.itemID / winLen;
			for (int item2Bin = 0; item2Bin <= interLen; item2Bin = item2Bin + rangeBins) {
				for (int item2Item = 0; item2Item < maxItem; item2Item++) {
					if (item1Item == item2Item) {
						continue;
					}
					short item2 = (short) (item2Item * winLen + item2Bin);
					BitSet item2TIDs = mapItemTIDs.get(item2);
					if (item2TIDs != null) {
						item2TIDs = (BitSet) item2TIDs.clone();
						item2TIDs.and(item1Node.wids);
						int item2NodeCounter = item2TIDs.cardinality();
						if (item2NodeCounter >= minsup[k - 2] && (saveCandidate() || item2NodeCounter >= minsup[k - 2])) {
							FPNode item2Node = new FPNode();
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
	FPNode getChild (List<FPNode> childs, int id) {
		int left = 0;
		int right = childs.size() - 1;

		while (left <= right) {
			int mid = left + (right - left) / 2;

			FPNode midNode = childs.get(mid);
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

	int getChildIndex (List<FPNode> childs, int id) {
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

	void generateCandidate3(FPNode node) throws IOException {
		prefixList.add(node.itemID);
		prefixSize++;
		if (prefixSize == 2) {
			int item2Bin = node.itemID % winLen;

			FPNode item2Node = getChild(root.childs, node.itemID - item2Bin);
			if (item2Node != null) {
				for (FPNode item3Node : item2Node.childs) {
					// for the current item
					if (prefixList.get(0) / winLen == item3Node.itemID / winLen) {
						continue;
					}
					int item3Bin = item3Node.itemID % winLen;
					if ((item2Bin + item3Bin) >= winLen) {
						break;
					}
					short item = (short) (item3Node.itemID + item2Bin);
					prefixList.add(item);
					prefixSize++;
					BitSet itemTIDs = mapItemTIDs.get(item);
					if (itemTIDs != null) {
						itemTIDs = (BitSet) itemTIDs.clone();
						itemTIDs.and(node.wids);
						int nextNodeCounter = itemTIDs.cardinality();
						if (nextNodeCounter >= minsup[k - 2] && (saveCandidate() || nextNodeCounter >= minsup[k - 2])) {
							FPNode nextNode = new FPNode();
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
			List<FPNode> nodeChilds = node.childs;
			int nodeChildsSize = nodeChilds.size();
			for (int iChild = 0; iChild < nodeChildsSize; iChild++) {
				// for the current item
				generateCandidate3(nodeChilds.get(iChild + nodeChilds.size() - nodeChildsSize));
			}
			prefixList.remove(prefixSize - 1);
			prefixSize--;
		}
	}

	public static long candidateToNeuronNumber(List<Short> candidate, int maxItem, int k, int winLen) {
		long number = candidate.get(0) / winLen * (long) Math.pow(maxItem, k - 1);
		for (int i = 1; i < k; i++) {
			number += candidate.get(i) / winLen * (long) Math.pow(maxItem, k - i - 1);
		}
		return number;
	}

	void generateCandidateK(FPNode node, int item2BinInput, FPNode item2NodeInput) throws IOException {
		prefixList.add(node.itemID);
		prefixSize++;
		if (prefixSize == k - 1) {
			for (FPNode itemLastNode : item2NodeInput.childs) {
				// for the current item
				if (prefixList.get(0) / winLen == itemLastNode.itemID / winLen) {
					continue;
				}
				int itemLastBin = itemLastNode.itemID % winLen;
				if ((item2BinInput + itemLastBin) >= winLen) {
					break;
				}
				short item = (short) (itemLastNode.itemID + item2BinInput);
				prefixList.add(item);
				prefixSize++;
				BitSet itemTIDs = mapItemTIDs.get(item);
				if (itemTIDs != null) {
					itemTIDs = (BitSet) itemTIDs.clone();
					itemTIDs.and(node.wids);
					int nextNodeCounter = itemTIDs.cardinality();
					if (k == maxPatternLength) {
						long candidateNeuronNumber = candidateToNeuronNumber(prefixList, maxItem, k, winLen);
						Integer maxSup = mapNeuronsMaxSup.get(candidateNeuronNumber);
						if (maxSup == null || nextNodeCounter > maxSup) {
							mapNeuronsMaxSup.put(candidateNeuronNumber, nextNodeCounter);
						}
					}
					if (nextNodeCounter >= minsup[k - 2] && (saveCandidate() || nextNodeCounter >= minsup[k - 2])) {
						FPNode nextNode = new FPNode();
						nextNode.itemID = item;
						nextNode.wids = itemTIDs;
						nextNode.counter = nextNodeCounter;
						node.addChild(nextNode);
					}
				}
				prefixList.remove(prefixSize - 1);
				prefixSize--;
			}
			prefixList.remove(prefixSize - 1);
			prefixSize--;
		}
		else {
			for (FPNode nextNode: node.childs) {
				FPNode item2Node;
				if (prefixSize > 1) {
					item2Node = getChild(item2NodeInput.childs, nextNode.itemID - item2BinInput);
				} else {
					item2BinInput = nextNode.itemID % winLen;
					item2Node = getChild(root.childs, (short) (nextNode.itemID - item2BinInput));
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
			System.out.printf("%d_%d_bg_%.2f_mt_%.2f_pp_%.1f_tj_%d_bin_%d_win_%d_inter_%d_range_%d_sup_%d_k_%d", motifType, recordingTime, backgroundFiringRate, motifFiringRate, pp, temporalJitter, binSize, this.winLen, this.interLen, rangeBins, minsup[k - 2], k);
			minsup[k - 2] += 1;
			for (FPNode rootChild : root.childs) {
				// for the current item
				prefixNodeList = new ArrayList<>();
				prefixNodeSize = 0;
				pruneCandidates(rootChild, k, root.childs);
			}
			System.out.printf("_freq_%d_time_%d_seed_%d\n", frequentCount, System.currentTimeMillis() - kTimestamp, seed);
			return false;
		}
		return true;
	}

	void pruneCandidates(FPNode node, int kPrune, List<FPNode> parentNodeChilds) throws IOException {
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
			List<FPNode> nodeChilds = node.childs;
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

	void cleanCandidates(FPNode node, int kPrune) {
		prefixNodeList.add(node);
		prefixNodeSize++;
		if (prefixNodeSize == kPrune - 1) {
			node.wids = null;
			if (node.childs == null || node.childs.isEmpty()) {
				List<FPNode> parentChilds;
				if (prefixNodeSize > 1) {
					parentChilds = prefixNodeList.get(prefixNodeSize - 2).childs;
				} else {
					parentChilds = root.childs;
				}
				parentChilds.remove(getChildIndex(parentChilds, node.itemID));
				if (parentChilds.isEmpty()) {
					for (int iChild = prefixNodeSize - 3; iChild >= 0; iChild--) {
						parentChilds = prefixNodeList.get(iChild).childs;
						FPNode childNode = prefixNodeList.get(iChild + 1);
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
			List<FPNode> nodeChilds = node.childs;
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
