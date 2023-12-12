### Scenario: "test 123"

#### Starting Conditions

* Memory Manager: "Fixed Segment Memory Manager"
* Real Memory: 2 Gig, divided into x segments of y bytes

#### Trace
* Process "P1" allocated x bytes
* Process "P2" allocated x bytes
* Process "P3" allocated x bytes

#### Ending Conditions
* Process "P1" has 2 segments, starting at
* Process "P2" has 2 segments, starting at

#### Real Memory:
* Memory in use: xx Meg
* Free memory:
   * Segment 2-10 (xx meg)
   * Segment 12-22 (xx meg)
* Fragmentation (ratio of used to to total memory): %



