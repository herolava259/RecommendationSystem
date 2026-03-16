

export interface VertexBase<TCore> {
  id: string;
  content: TCore;
}


export interface EdgeBase<TCore> {
  sourceId: string;
  targetId: string;
  content: TCore;
}

export abstract class SchemaGraph {

  vertexes: Set<string> = new Set<string>();

  edges: Set<string> = new Set<string>();

  adjList: Map<string, string[]> = new Map<string, string[]>();


  public addVertex(vertexId: string): boolean{

    if(this.vertexes.has(vertexId))
      return false;
      //throw error

    this.vertexes.add(vertexId);
    return true;

  }

  public addEdge(sourceId: string, targetId: string): boolean{

    const edgeId = `${sourceId}->${targetId}`;

    if(this.edges.has(edgeId))
      return false;

    this.edges.add(edgeId);

    this.adjList.set(sourceId, [...(this.adjList.get(sourceId) || []), targetId]);

    return true;
  }

  public abstract removeEdge(edgeId: string): boolean;

  public abstract removeEdge(sourceId: string, targetId: string): boolean;

  public abstract removeVertex(vertexId: string): boolean;

  public existVertex(vertexId: string): boolean {
    return this.vertexes.has(vertexId);
  }

  public existEdge(sourceId: string, targetId: string): boolean {

    const edgeId = `${sourceId}->${targetId}`;
    return this.edges.has(edgeId);
  }

  // TODO: implement alg in graph below

}


export abstract class BiDirectionalSchemaGraph extends SchemaGraph {

  public override addEdge(sourceId: string, targetId: string): boolean {

    const edgeIdOne = `${sourceId}<->${targetId}`;
    const edgeIdTwo = `${targetId}<->${sourceId}`;

    if(this.edges.has(edgeIdOne) || this.edges.has(edgeIdTwo))
      return false;

    this.edges.add(edgeIdOne);

    this.adjList.set(sourceId, [...(this.adjList.get(sourceId) || []), targetId]);
    this.adjList.set(targetId, [...(this.adjList.get(targetId) || []), sourceId]);

    return true;
  }

  public override removeEdge(edgeId: string): boolean {

    if(!this.edges.has(edgeId))
      return false;

    this.edges.delete(edgeId);
    return true;
  }

  public override existEdge(sourceId: string, targetId: string): boolean {

    const edgeIdOne = `${sourceId}<->${targetId}`;
    const edgeIdTwo = `${targetId}<->${sourceId}`;

    return this.edges.has(edgeIdOne) || this.edges.has(edgeIdTwo);

  }

}

export abstract class VertexCoreGraph<TCore> extends SchemaGraph {

  protected vertexCoreMap: Map<string, TCore> = new Map<string, TCore>();
}

export abstract class EdgeCoreGraph<TCore> extends SchemaGraph {

  protected edgeCoreMap: Map<string, TCore> = new Map<string, TCore>();
}

export abstract class VertexEdgeCoreGraph<TVertexCore, TEdgeCore> extends SchemaGraph {

  protected vertexCoreMap: Map<string, TVertexCore> = new Map<string, TVertexCore>();

  protected edgeCoreMap: Map<string, TEdgeCore> = new Map<string, TEdgeCore>();
}
