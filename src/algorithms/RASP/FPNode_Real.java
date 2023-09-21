package algorithms.RASP;

import java.util.ArrayList;
import java.util.BitSet;
import java.util.List;

public class FPNode_Real {
	int itemID;
	BitSet wids;
	int counter;  // frequency counter  (a.k.a. support)
	
	// the child nodes of that node
	List<FPNode_Real> childs;

	FPNode_Real(){	}

	void addChild (FPNode_Real addedNode) {
		if (childs == null) {
			childs = new ArrayList<>();
		}
		childs.add(addedNode);
	}
}
