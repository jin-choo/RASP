package main;

import algorithms.RASP.RASP_Case;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.text.SimpleDateFormat;
import java.util.ArrayList;

public class Main_saveToFile_Case {

	public static void main(String [] arg) throws IOException{
		ArrayList<String> filePathList = new ArrayList<>() {{ add("yoochoose-clicks_crop"); }};
		ArrayList<int[]> timeItemLengthBinWinlenInterlenRangebinsList = new ArrayList<>() {{
			add(new int[]{1440, 100, 3, 60, 10, 9, 1});
			add(new int[]{86400, 100, 3, 1, 600, 599, 5});
		}};

		ArrayList<ArrayList> totalList = new ArrayList<>() {{ add(filePathList); add(timeItemLengthBinWinlenInterlenRangebinsList); }};
		ArrayList<ArrayList> productList = cartesianProduct(0, totalList);
		productList.stream().forEach( resultList -> {
			String filePath = (String) resultList.get(1);
			int[] timeItemLengthBinWinlenInterlenRangebins = (int[]) resultList.get(0);
			int time = timeItemLengthBinWinlenInterlenRangebins[0];
			int item = timeItemLengthBinWinlenInterlenRangebins[1];
			int length = timeItemLengthBinWinlenInterlenRangebins[2];
			int binsize = timeItemLengthBinWinlenInterlenRangebins[3];
			int winlen = timeItemLengthBinWinlenInterlenRangebins[4];
			int interlen = timeItemLengthBinWinlenInterlenRangebins[5];
			int rangeBins = timeItemLengthBinWinlenInterlenRangebins[6];

			long timestamp = System.currentTimeMillis();
			BufferedWriter writerTime = null;
			try {
				Files.createDirectories(Paths.get(String.format("./txt/datasets/ecommerce/time_tree_tid/", filePath)));
				writerTime = new BufferedWriter(new FileWriter(String.format("./txt/datasets/ecommerce/time_tree_tid/%s_time_%d_item_%d_length_%d_bin_%d_winlen_%d_interlen_%d_rangebins_%d_%s.csv", filePath, time, item, length, binsize, winlen, interlen, rangeBins, new SimpleDateFormat( "MM.dd_HH.mm").format(timestamp))));
				writerTime.write("filePath,time,session,item,length,bin,winlen,interlen,rangebins,sup,k,#cand,#freq,time");
				writerTime.newLine();
				writerTime.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
			try {
				RASP_Case algo = new RASP_Case();
				algo.runAlgorithm(filePath, time, item, length, binsize, winlen, interlen, rangeBins, timestamp);
				algo.printStats();
			} catch (OutOfMemoryError oome) {
				System.out.println(String.format("%s_time_%d_item_%d_length_%d_bin_%d_winlen_%d_interlen_%d_rangebins_%d", filePath, time, item, length, binsize, winlen, interlen, rangeBins));
				System.err.println("Max JVM memory: " + Runtime.getRuntime().maxMemory());
			} catch (Exception e) {
				System.out.println(String.format("%s_time_%d_item_%d_length_%d_bin_%d_winlen_%d_interlen_%d_rangebins_%d", filePath, time, item, length, binsize, winlen, interlen, rangeBins));
				e.printStackTrace();
			}
		});
	}

	public static ArrayList<ArrayList> cartesianProduct(int index, ArrayList<ArrayList> lists) {
		ArrayList<ArrayList> ret = new ArrayList<>();
		if (index == lists.size()) {
			ret.add(new ArrayList());
		} else {
			for (Object obj : lists.get(index)) {
				for (ArrayList set : cartesianProduct(index+1, lists)) {
					set.add(obj);
					ret.add(set);
				}
			}
		}
		return ret;
	}
}
