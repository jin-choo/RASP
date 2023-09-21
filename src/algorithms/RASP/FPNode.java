package algorithms.RASP;

import java.util.*;

public class FPNode {
	short itemID;
	BitSet wids;
	int counter;  // frequency counter  (a.k.a. support)

	// the child nodes of that node
	List<FPNode> childs;

	FPNode(){ }

	void addChild (FPNode addedNode) {
		if (childs == null) {
			childs = new ArrayList<>();
		}
		childs.add(addedNode);
	}
}