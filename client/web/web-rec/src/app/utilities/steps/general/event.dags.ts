



export class EventDags {
  private adjList = new Map<string, string[]>();

  addEventVertex(eventId: string)
  {
    if (this.adjList.has(eventId)) {
      return;
    }
    this.adjList.set(eventId, []);
  }

  addEventEdge(sourceEventId: string, targetEventId: string){

    this.addEventVertex(sourceEventId);
    this.addEventVertex(targetEventId);

    this.adjList.get(sourceEventId)?.push(targetEventId);
  }

  getDependentEvents(eventId: string): string[] {
    return this.adjList.get(eventId) || [];
  }

}
